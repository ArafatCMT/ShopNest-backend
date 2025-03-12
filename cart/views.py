from django.shortcuts import render
from . import models
from products.models import Product
from . import serializers
from users.models import Customer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
# Create your views here.

# cart e item add r item er quantity ei view er maddhomei hocca
class AddToCartView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound({"detail":"product dosn't exist"})

    def post(self, request, pk):
        # print(request.user)
        product = self.get_object(pk)
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"error":"Customer dosn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        # filter kortaci cart e product ta already add kora ase  ki nai
        is_exist = models.Cart.objects.filter(product=product, customer=customer).exists()
        # jodi cart e product ta already add kora thake tobe shudu quantity ta 1 increase kore dicci 
        if is_exist:
            cart_item = models.Cart.objects.get(product=product, customer=customer)

            # Cart er quantity jodi available stock er theke beshi hoy, taile check korbe
            if cart_item.quantity + 1 > product.quantity:
                return Response(
                    {"error": "Insufficient stock available."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * cart_item.total_price
            cart_item.save()

            return Response({
                "message": "Cart item updated successfully.",
                "cart_item": serializers.CartSerializer(cart_item).data
            }, status=status.HTTP_200_OK)

        # cart e add na thakle abr notun object create hobe
        data = {
            "product": product.id,
            "customer": customer.id,
            "total_price": product.price
            }
        # print(data)
        serializer = serializers.CartSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RemoveToCartView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer account not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = models.Cart.objects.get(pk=pk)
        except models.Cart.DoesNotExist:
            return Response({"detail":"Cart item not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # check korteci je ei cart item ta current loggin-user er ki na. jodi na hoi tobe ei cart item ta remove korar tar permission nai
        if cart_item.customer != customer:
            return Response({"error":"You can only remove items from your own cart."}, status=status.HTTP_400_BAD_REQUEST)
        
        # cart item ta jodi current loggin-user er hoi tobei cart item ta remove hobe
        cart_item.delete()
        return Response({"detail":"Cart item remove successfully"}, status=status.HTTP_200_OK)
    

class CartItemQuantityDecreaseView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get(self, request, pk):
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer account not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = models.Cart.objects.get(pk=pk)
        except models.Cart.DoesNotExist:
            return Response({"detail":"Cart item not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # check korteci je ei cart item ta current loggin-user er ki na. jodi na hoi tobe ei cart item ta modify korar tar permission nai
        if cart_item.customer != customer:
            return Response({"error":"You can only modify items in your own cart."}, status=status.HTTP_400_BAD_REQUEST)
        
        if cart_item.quantity == 1:
            return Response({"error": "Quantity cannot be decreased below 1."}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = cart_item.quantity - 1
        cart_item.total_price = cart_item.quantity * cart_item.product.price
        cart_item.save()
        return Response({"success":"Item quantity has been decreased."}, status=status.HTTP_200_OK)


class CustomerCartDetailView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"error":"Customer doesn't exist"})
        
        cart_list = models.Cart.objects.filter(customer=customer)
        print(cart_list)
        serializer = self.serializer_class(cart_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)