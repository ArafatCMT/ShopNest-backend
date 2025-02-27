from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddCategory.as_view(), name='addCategory'),
]