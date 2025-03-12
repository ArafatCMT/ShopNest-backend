from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='order-view-set'), # get : api/orders/?status=Pending
router.register(r'customer-orders', views.CustomerOrderViewSet) # get : api/customer-orders/?status=Pending

urlpatterns = [
    path('checkout/', views.CheckOutView.as_view(), name='check-out'), # post
    path('', include(router.urls)), 
    path('order/update/<int:pk>/', views.OrderStatusUpdateView.as_view(), name='order-status-update'), # patch, api/order/update/<int:order_id>/
]