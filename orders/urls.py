from django.urls import path
from .views import CreateOrderAPI

urlpatterns = [
    path("create-order/", CreateOrderAPI.as_view())
]