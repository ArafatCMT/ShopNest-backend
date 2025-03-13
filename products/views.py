from django.shortcuts import render
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . models import Product
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from categories.models import Category
from rest_framework import filters

# Create your views here.
class AddProductView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.ProductSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound(detail="Product doesn't exist")
            
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductUpdateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.ProductSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound(detail="Product doesn't exist")
        
    def patch(self, request, pk):
        product = self.get_object(pk)
        # je sob fields update kora jbe
        allowed_fields = ['name', 'product_img_url', 'discription', 'price', 'category', 'brand', 'color', 'quantity']

        # check kortaci allowed_fields er value cara onno kono value ase ki na , shudu allowed_fields er value gula i nebe onno thai ek ta {} dictonary update_data te assign hobe
        update_data = {key:value for key,value in request.data.items() if key in allowed_fields}
        print(update_data)

        if not update_data:
            return Response({"error": "No valid fields provided for update."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(product, data=update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDeleteView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.ProductSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound(detail="Product doesn't exist")
        
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)
    

class AllProductsView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name'] # Product er name er opor vitti kore product search hobe


class CategoryWiseProductView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductSerializer

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise NotFound(detail="Category doesn't exist")
        
    def get(self, request, category_slug):
        category = self.get_object(category_slug)
        products = Product.objects.filter(category=category)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

