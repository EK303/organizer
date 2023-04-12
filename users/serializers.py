from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import TrelloUser
from .tokens import send_activation_code


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()


class UserRegisterSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=30, allow_blank=True, default=None)
    last_name = serializers.CharField(max_length=30, allow_blank=True, default=None)
    username = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(max_length=30, required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, validated_data):
        # validating email
        if TrelloUser.objects.filter(email=validated_data.get("email")).exists():
            raise serializers.ValidationError("This email already exists")
        #validating username
        if TrelloUser.objects.filter(username=validated_data.get("username")).exists():
            raise serializers.ValidationError("This username already exists")
        # validating passwords
        password1 = validated_data.get("password1")
        password2 = validated_data.get("password2")
        if password1 != password2:
            raise serializers.ValidationError("Passwords don't match")
        return validated_data

    def create(self, validated_data):
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password1")
        user = TrelloUser.objects.create_user(first_name=first_name,
                                              last_name=last_name,
                                              username=username,
                                              email=email,
                                              password=password)

        user.is_active = False

        send_activation_code(email=user.email, activation_code=user.activation_code)

        return user


class ActivateAccountSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    activation_code = serializers.CharField()


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username,
                                password=password)
            if not user:
                message = 'Unable to log in with the provided credentials'
                raise serializers.ValidationError(message, code="authorization")
        else:
            message = 'Must include "username" and "password".'
            raise serializers.ValidationError(message, code="authorization")
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
