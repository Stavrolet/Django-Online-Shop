from django.urls import path
from .views import CategoriesApi, ProductApi, ProductsApi

urlpatterns = [
    path("categories/", CategoriesApi.as_view()),
    path("search/", ProductsApi.as_view()),
    path("products/<slug:category_slug>/", ProductsApi.as_view()),
    path("product/<slug:product_slug>/", ProductApi.as_view()),
    path("product/", ProductApi.as_view()),
]