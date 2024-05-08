from django.test import TestCase
from django.utils import timezone
from vendors.models import Vendor, PurchaseOrder

class PerformanceMetricsTestCase(TestCase):
    def setUp(self):
        # Create a vendor
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@example.com",
            address="123 Test St",
            vendor_code="TEST123"
        )

    def test_quality_rating_average(self):
        # Create completed purchase orders with quality ratings
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            quality_rating=4,
            status='completed'
        )
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            quality_rating=5,
            status='completed'
        )
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            quality_rating=3,
            status='completed'
        )

        # Calculate quality rating average
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.quality_rating_avg, 4)  # Average of 4, 5, and 3 is 4

    def test_average_response_time(self):
        # Create completed purchase orders with acknowledgment dates
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            issue_date=timezone.now() - timezone.timedelta(days=1),
            acknowledgment_date=timezone.now(),  # Acknowledged in 1 day
            status='completed'
        )
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            issue_date=timezone.now() - timezone.timedelta(days=2),
            acknowledgment_date=timezone.now(),  # Acknowledged in 2 days
            status='completed'
        )

        # Calculate average response time
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.average_response_time, 1.5)  # Average of 1 and 2 is 1.5 days

    def test_fulfillment_rate(self):
        # Create completed purchase orders with varying statuses
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            status='completed'
        )
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            status='completed'
        )
        PurchaseOrder.objects.create(
            vendor=self.vendor,
            status='canceled'
        )

        # Calculate fulfillment rate
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.fulfillment_rate, 66.67)  # 2 out of 3 orders completed, should be 66.67%
# Similar tests for other performance metrics (quality rating average, average response time, fulfillment rate)