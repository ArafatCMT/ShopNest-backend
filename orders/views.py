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
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
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


# Shipped mail function
def send_shipment_email(customer, product ):
    email_subject = "Your Order Has Been Shipped! 🚚📦"
    email_body = render_to_string('shipped_mail.html', {'customer_name': customer.user.first_name, 'product_name':product.name})
    email = EmailMultiAlternatives(
            subject=email_subject,
            body="",
            from_email=settings.EMAIL_HOST_USER,
            to=[customer.user.email]
        )
    email.attach_alternative(email_body, "text/html")
    email.send()

# delivered mail function
def send_delivery_email(customer, product ):
    email_subject = "Your Order Has Been Delivered! 🎉"
    email_body = render_to_string('delivered_mail.html', {'customer_name': customer.user.first_name, 'product_name':product.name})
    email = EmailMultiAlternatives(
            subject=email_subject,
            body="",
            from_email=settings.EMAIL_HOST_USER,
            to=[customer.user.email]
        )
    email.attach_alternative(email_body, "text/html")
    email.send()

class OrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]
    # serializer_class = serializers.OrderSerializer

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise NotFound({"detail":"Order not found."})

    def patch(self, request, pk):
        order = self.get_object(pk)
        # jodi order status pending, canceled, ba delivered hoi tobe order status update kora hobe na 
        if order.order_status in ['Pending', 'Canceled', 'Delivered']:
            return Response({
                "message": "The order is either pending, canceled, or delivered. Status update is not allowed."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # check kortaci order status cara onno kono field provide kora hoica ki na 
        if not 'order_status' in request.data:
            return Response({
                "error": "Only 'order_status' can be updated."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Validating the status update
        valid_statuses = ['Shipped', 'Delivered']
        new_status = request.data.get('order_status')

        # check kortaci order status empty ase ki na , ei ta empty rakha jabe na 
        if not new_status:
            return Response({"error": "Order status is required."}, status=status.HTTP_400_BAD_REQUEST)

        # check kortaci jei status ta provide kora hoiva oi ta valid status ki na 
        if new_status not in valid_statuses:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        
        # order status jodi Processing thake tobe order status Shipped hobe 
        if order.order_status == 'Processing' and new_status == 'Shipped':
            order.order_status = new_status
            # email function call hobe
            send_shipment_email(order.customer, order.product)
            print("Shipped")
            pass

        # order status jodi shipped thake tobe order status delivered hobe r is delivered true hobe 
        elif order.order_status == 'Shipped' and new_status == 'Delivered':
            order.order_status = new_status
            # email function call hobe
            order.is_delivered = True
            send_delivery_email(order.customer, order.product)
            print("Delivered")
            pass

        serializer = serializers.OrderSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  # Save the updated order
            return Response({
                "message": "Order status updated successfully.",
                "order": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    