from django.urls import path
from . import views

urlpatterns = [
    path('product/add/', views.AddProductView.as_view(), name='add_product'), # post
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'), # get
    path('product/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'), # patch
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'), # delete
    path('products/', views.AllProductsView.as_view(), name='all_products'), # get
    path('product/category/<category_slug>/', views.CategoryWiseProductView.as_view(), name='category_wise_product'), # get
]