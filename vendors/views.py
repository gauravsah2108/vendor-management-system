from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from rest_framework import generics
from rest_framework.response import Response
from .serializers import VendorSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import VendorPerformanceSerializer
from django.utils import timezone

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        performance_data = {
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': instance.quality_rating_avg,
            'average_response_time': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate
        }
        return Response(performance_data)
    

def vendor_performance(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    serializer = VendorPerformanceSerializer(vendor)
    return JsonResponse(serializer.data)

def acknowledge_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()
    # Trigger recalculation of average_response_time for the vendor
    vendor = purchase_order.vendor
    vendor.calculate_average_response_time()
    return JsonResponse({'message': 'Purchase order acknowledged successfully.'})