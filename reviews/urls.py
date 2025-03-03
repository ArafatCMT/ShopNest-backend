from django.urls import path
from . import views

urlpatterns = [
    path('review-add/', views.AddReviewView.as_view(), name='add-review'),
    path('review/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]