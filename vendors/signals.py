from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, ExpressionWrapper, F, FloatField, Count, Value, Case, When
from .models import PurchaseOrder, Vendor

@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    if not created and instance.status_changed:
        vendor = instance.vendor

        # Calculate and update on-time delivery rate
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_orders = completed_orders.count()
        
        if total_completed_orders > 0:
            on_time_deliveries = completed_orders.filter(delivery_date__lte=F('acknowledgment_date')).count()
            on_time_delivery_rate = (on_time_deliveries / total_completed_orders) * 100
        else:
            on_time_delivery_rate = 0

        vendor.on_time_delivery_rate = on_time_delivery_rate

        # Calculate and update quality rating average
        completed_orders_with_rating = completed_orders.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_orders_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0
        vendor.quality_rating_avg = quality_rating_avg

        # Calculate and update average response time
        acknowledged_orders = completed_orders.filter(acknowledgment_date__isnull=False)
        response_time = ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=FloatField())
        average_response_time = acknowledged_orders.annotate(response_time=response_time).aggregate(avg_response_time=Avg('response_time'))['avg_response_time'] or 0
        vendor.average_response_time = average_response_time

        # Calculate and update fulfillment rate
        successfully_fulfilled_orders = completed_orders.filter(issue_date__lte=F('acknowledgment_date'))
        total_orders = completed_orders.count()

        if total_orders > 0:
            fulfillment_rate = (successfully_fulfilled_orders.count() / total_orders) * 100
        else:
            fulfillment_rate = 0

        vendor.fulfillment_rate = fulfillment_rate

        vendor.save()
