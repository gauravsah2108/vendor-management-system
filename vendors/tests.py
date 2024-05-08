from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(name="Vendor 1", contact_details="vendor1@example.com", address="123 Street", vendor_code="VENDOR001")
        self.vendor2 = Vendor.objects.create(name="Vendor 2", contact_details="vendor2@example.com", address="456 Street", vendor_code="VENDOR002")
        self.purchase_order1 = PurchaseOrder.objects.create(vendor=self.vendor1, po_number="PO001", status="pending")
        self.purchase_order2 = PurchaseOrder.objects.create(vendor=self.vendor1, po_number="PO002", status="completed")

    def test_get_vendors_list(self):
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_vendor_details(self):
        response = self.client.get(f'/api/vendors/{self.vendor1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Vendor 1")

    def test_create_vendor(self):
        data = {'name': 'New Vendor', 'contact_details': 'newvendor@example.com', 'address': '789 Street', 'vendor_code': 'NEWVENDOR001'}
        response = self.client.post('/api/vendors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 3)

    def test_update_vendor(self):
        data = {'name': 'Updated Vendor'}
        response = self.client.put(f'/api/vendors/{self.vendor1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.get(id=self.vendor1.id).name, 'Updated Vendor')

    def test_delete_vendor(self):
        response = self.client.delete(f'/api/vendors/{self.vendor1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 1)
