from django.urls import path
from . import views

urlpatterns = [
    path('admin/login/', views.AdminLoginView.as_view(), name='adminLogin'), # post
    path('admin/profile/', views.AdminProfileView.as_view(), name='adminLogin'), # get, patch
]