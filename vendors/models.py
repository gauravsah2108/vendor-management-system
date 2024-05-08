from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Vendor, PurchaseOrder
from datetime import timedelta
# from .vendor import Vendor

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_deliveries = completed_orders.filter(delivery_date__lte=instance.delivery_date).count()
        total_completed_orders = completed_orders.count()
        if total_completed_orders > 0:
            on_time_delivery_rate = on_time_deliveries / total_completed_orders * 100
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if instance.quality_rating is not None and instance.status == 'completed':
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_ratings = sum(order.quality_rating for order in completed_orders if order.quality_rating is not None)
        total_completed_orders = completed_orders.count()
        if total_completed_orders > 0:
            quality_rating_avg = total_ratings / total_completed_orders
            vendor.quality_rating_avg = quality_rating_avg
            vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date is not None:
        vendor = instance.vendor
        acknowledged_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        total_response_time = timedelta(0)
        total_acknowledged_orders = 0
        for order in acknowledged_orders:
            response_time = order.acknowledgment_date - order.issue_date
            total_response_time += response_time
            total_acknowledged_orders += 1
        if total_acknowledged_orders > 0:
            average_response_time = total_response_time / total_acknowledged_orders
            vendor.average_response_time = average_response_time.total_seconds() / 3600  # Convert timedelta to hours
            vendor.save()

@receiver([post_save, post_delete], sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, **kwargs):
    vendor = instance.vendor
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    if total_orders > 0:
        fulfillment_rate = (fulfilled_orders / total_orders) * 100
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()