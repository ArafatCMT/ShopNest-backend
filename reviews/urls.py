from django.urls import path
from . import views

urlpatterns = [
    path('review-add/', views.AddReviewView.as_view(), name='add-review'), # post
    path('review/update/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'), # get, patch, delete
    path('reviews/product/<int:pk>/', views.SpecificProductReviewsView.as_view(), name='specific-product-reviews'), # get
]