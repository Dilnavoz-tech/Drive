import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, MyTokenObtainPairSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        responses={201: RegisterSerializer()},
        operation_summary="User Registration",
        operation_description="Register a new user and return JWT tokens.",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)



class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(
        responses={200: MyTokenObtainPairSerializer()},
        operation_summary="User Login",
        operation_description="Authenticate a user and return JWT tokens.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="User Logout",
        operation_description="Blacklist the user's refresh token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
            },
            required=['refresh'],
        ),
        responses={
            205: 'Token blacklisted',
            400: 'Bad Request - Invalid token or missing parameter',
        },
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logging.error(f"Error during logout: {str(e)}")  # Log the error
            return Response(status=status.HTTP_400_BAD_REQUEST)




