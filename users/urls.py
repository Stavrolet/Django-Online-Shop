from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginAPI, LogoutAPI, RegistrationAPI, UserInfoAPI

urlpatterns = [
    path("registration/", RegistrationAPI.as_view()),
    path("profile/", UserInfoAPI.as_view()),
    path("token/", LoginAPI.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", LogoutAPI.as_view()),
]