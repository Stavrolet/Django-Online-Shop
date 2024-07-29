from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from django.forms import ValidationError
from carts.models import Cart
from orders.models import Order, OrderItem

# Create your views here.

class CreateOrderAPI(APIView):
    def post(self, request):
        # try:
        with transaction.atomic():
            user = request.user
            carts = Cart.objects.filter(user=user)

            if carts.exists():
                order = Order.objects.create(
                    user=user,
                    phone_number=request.data["phone_number"],
                    requires_delivery=request.data["requires_delivery"],
                    delivery_address=request.data["delivery_address"],
                    payment_on_get=request.data["payment_on_get"],
                )

                for cart in carts:
                    product = cart.product
                    name = cart.product.name
                    price = cart.product.final_price()
                    quantity = cart.quantity

                    if product.quantity < quantity:
                        raise Exception(
                            f"Insufficient quantity of {name} in stock/In stock - {quantity}"
                        )

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        name=name,
                        price=price,
                        quantity=quantity,
                    )
                    product.quantity -= quantity
                    product.save()

                carts.delete()
                return Response(status=status.HTTP_202_ACCEPTED)