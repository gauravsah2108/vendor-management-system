from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet
from .views import PurchaseOrderViewSet
from .views import VendorPerformanceAPIView
from . import views

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<int:pk>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge_purchase_order'),
]

# urlpatterns = [
#     path('api/vendors/<int:pk>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
# ]

