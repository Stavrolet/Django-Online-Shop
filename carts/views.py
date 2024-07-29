from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from carts.models import Cart
from carts.serializers import CartSerializer
from products.models import Product

# Create your views here.

class CartAddAPI(APIView):
    def get(self, request):
        product = Product.objects.get(slug=request.query_params.get("product_slug", None))
        cart_for_response = None

        if request.user.is_authenticated:
            carts = Cart.objects.filter(user=request.user, product=product)

            if carts.exists():
                cart = carts.first()
                if cart:
                    cart.quantity += 1
                    cart.save()
                    cart_for_response = cart
            else:
                Cart.objects.create(user=request.user, product=product, quantity=1)
        else:
            if not request.session.session_key:
                request.session.create()
                
            carts = Cart.objects.filter(session_key=request.session.session_key, product=product)

            if carts.exists():
                cart = carts.first()
                if cart:
                    cart.quantity += 1
                    cart.save()
                    cart_for_response = cart
            else:
                cart_for_response = Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)
        
        serializer = CartSerializer(cart_for_response)
        return Response(serializer.data)

class CartRemoveAPI(APIView):
    def get(self, request):
        try:
            cart = Cart.objects.get(id=request.query_params.get("cart_id", None))
            cart.delete()
            return Response({"message": "Cart was successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
class CartGetAPI(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data) 
        elif not request.session.session_key:
            request.session.create()
            return Response({"message": "Session was successfully created. There are no carts for this session"}, status=status.HTTP_204_NO_CONTENT)
        else:
            cart = Cart.objects.filter(session_key=request.session.session_key)
            if not cart:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data)