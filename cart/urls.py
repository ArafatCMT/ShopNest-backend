from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/<int:pk>/', views.AddToCartView.as_view(), name='add-cart'), # post, <int:product.id>
    path('cart/list/', views.CustomerCartDetailView.as_view(), name='cart-list') , # get
    path('cart/remove/<int:pk>/', views.RemoveToCartView.as_view(), name='cart-remove') , # delete
    path('cart/item/decrease-quantity/<int:pk>/', views.CartItemQuantityDecreaseView.as_view(), name='cart-item-desrease') , # get
]