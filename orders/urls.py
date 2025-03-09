from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.CheckOutView.as_view(), name='check-out'), # post
    path('orders/pending/', views.PendingOrderListView.as_view()), # get
]