from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from . import serializers
from users import models
from cart.models import Cart
from orders.models import Order
from cart.serializers import CartSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import pagination, filters
# Create your views here.
class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            customer = models.Customer.objects.get(user=request.user)
        except models.Customer.DoesNotExist:
            return Response({"detail":"user doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items = Cart.objects.filter(customer=customer)

        if cart_items.exists():
            for item in cart_items:
                # print(item.product, item.quantity, item.total_price)

                data = {
                    'customer':customer.id,
                    'product':item.product.id,
                    'quantity':item.quantity,
                    'total_amount':item.total_price
                }

                serializer = serializers.OrderSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    cart_items.delete()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"detail": "Order placed successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        

class find_orders_for_customer(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        status = request.query_params.get('status')
        try:
            customer = models.Customer.objects.get(user=request.user)
        except models.Customer.DoesNotExist:
            return queryset.none()

        if status:
            return queryset.filter(order_status=status, customer=customer)
        return queryset.filter(customer=customer)

            
class CustomerOrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [find_orders_for_customer]

    # def get(self, request):
    #     try:
    #         customer = models.Customer.objects.get(user=request.user)
    #     except models.Customer.DoesNotExist:
    #         return Response({"detail":"user doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
        
    #     pending_orders = Order.objects.filter(customer=customer, order_status='Pending')
        
    #     if not pending_orders.exists():
    #         return Response({"detail": "No pending orders found."}, status=status.HTTP_404_NOT_FOUND)
        
    #     serializer = serializers.OrderSerializer(pending_orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class Find_status_wise_orders(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        status = request.query_params.get('status')
        # print(status)
        if status:
            return queryset.filter(order_status=status)
        return queryset

class OrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [Find_status_wise_orders]

    