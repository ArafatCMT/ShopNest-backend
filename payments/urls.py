from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.Payment),
    path('payment-successfull/<int:customer_id>/', views.payment_successfull),
    path('payment-failed/<int:customer_id>/', views.payment_failed),
]