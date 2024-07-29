from django.urls import path
from .views import *

urlpatterns = [
    path("cart-add/", CartAddAPI.as_view()),
    path("cart-remove/", CartRemoveAPI.as_view()),
    path("cart-get/", CartGetAPI.as_view()),
]