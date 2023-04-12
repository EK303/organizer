from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from drf_yasg.utils import swagger_auto_schema

from .serializers import UserRegisterSerializer, LoginSerializer, ActivateAccountSerializer, ChangePasswordSerializer
from .models import TrelloUser


# Create your views here.

class RegisterUserView(APIView):
    permission_classes = []

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request):
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully signed up', status=status.HTTP_201_CREATED)


class ActivateView(APIView):

    permission_classes = []

    @swagger_auto_schema(request_body=ActivateAccountSerializer)
    def post(self, request):
        username = request.data['username']
        user = get_object_or_404(TrelloUser, username=username)
        activation_code = request.data['activation_code']
        if user.activation_code != activation_code:
            return Response("Invalid activation code", status=status.HTTP_403_FORBIDDEN)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response("Your account has been activated", status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)


class PasswordChangeView(APIView):

    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_password = request.data['password1']
            user = request.user
            if user.check_password(new_password):
                return Response("New password should not match the old one", status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response("Password changed", status=status.HTTP_201_CREATED)

