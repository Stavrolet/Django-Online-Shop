from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.serializers import UserSerializer
from carts.models import Cart

class RegistrationAPI(APIView):
    def post(self, request): 
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoAPI(APIView):
    def get(self, request):
        email = request.query_params.get("username", None)
        if email:
            user = User.objects.get(username=email)
            if not user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutAPI(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPI(TokenObtainPairView):
    def post(self, request: Request, *args, **kwards):
        if request.session.session_key:
            user = User.objects.get(username=request.data["username"])
            Cart.objects.filter(session_key=request.session.session_key).update(user=user, session_key=None)
        return super().post(request, *args, **kwards)