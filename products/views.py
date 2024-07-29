from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategoriesSerializer, ProductsSerializer
from .utils import q_search

class CategoriesApi(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

class ProductsApi(APIView):
    def get(self, request, category_slug = None):
        query = request.query_params.get("q", None)
        on_sale = request.query_params.get("on_sale", None)
        order_by = request.query_params.get("order_by", None)
        max_price = request.query_params.get("max_price", None)
        min_price = request.query_params.get("min_price", None)
        
        if category_slug == "all":
            products_list = Product.objects.all()
        elif query:
            products_list = q_search(query)
        else:
            products_list = Product.objects.filter(category__slug=category_slug)
        
        if on_sale == "on":
            products_list = products_list.filter(discount__gt=0)
            
        if order_by and order_by != "default":
            products_list = products_list.order_by(order_by)
            
        if min_price:
            products_list = products_list.filter(price__gt=min_price)
        elif max_price:
            products_list = products_list.filter(price__lt=max_price)
        elif min_price and max_price:
            products_list = products_list.filter(Q(price__gt=min_price) | Q(price__lt=max_price))

        serializer = ProductsSerializer(products_list, many=True)
        return Response(serializer.data)
    
class ProductApi(APIView):
    def get(self, request, product_slug=None):
        product_id = request.query_params.get("product_id", None)
        if product_id:
            product = Product.objects.get(id=product_id)
        else:
            product = Product.objects.get(slug=product_slug)
            
        serializer = ProductsSerializer(product)
        return Response(serializer.data)