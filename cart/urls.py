from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/<int:pk>/', views.AddToCartView.as_view(), name='add-cart'), # post
    path('cart/list/', views.CustomerCartDetailView.as_view(), name='cart-list') , # get
]