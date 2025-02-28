from django.urls import path
from . import views

urlpatterns = [
    path('category/add/', views.AddCategory.as_view(), name='addCategory'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='detailView'),
]