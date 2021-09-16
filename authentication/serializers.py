from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied

from .models import User
from .utils import Util

from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True) #write_only so not to expose the password in json data

    class Meta:
        model = User
        fields = ['email', 'username','password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should only contian alpanumeric chars'
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create(**validated_data)

class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=8)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)


    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')

        
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            raise NotFound('User not found')
            
        auth.authenticate(username=user.username)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        context = {
            'email' : user.email,
            'username' : user.username,
            'tokens': user.tokens(),
        }
        return context
'''
class RefreshTokensSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5)
    username = serializers.CharField(min_length=5)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        fields = ['email', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')

        try:
            user = User.objects.get(email=email, username=username)
        except User.DoesNotExist:
            raise NotFound('User not found')

        if not user.is_active:
            raise PermissionDenied('Account disabled, contact admin')
        if not user.is_verified:
            raise PermissionDenied('Email is not verified')

        context = {
            'email' : user.email,
            'username' : user.username,
            'tokens': user.tokens(),
        }
        return context
'''
class RequestPasswordRestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5)

    class Meta:
        fields = ['email']

    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password','token','uidb64']

    def validate(self, attrs):
        password = attrs.get('password')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return (user)
        except DjangoUnicodeDecodeError as indentifier:
            raise AuthenticationFailed('The reset link is invalid', 401)
