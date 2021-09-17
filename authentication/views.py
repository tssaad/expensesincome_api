import datetime
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework import permissions


from .serializers import *
from .models import User
from .utils import Util
from .renderers import UserRenderer

from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        # get new created user
        user = User.objects.get(email=user_data['email'])
        # create fresh toekn for user
        token = RefreshToken.for_user(user).access_token

        # get current site
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = "http://"+current_site+relative_link+"?token="+str(token)

        # preparing data to send verification email
        email_subject = 'Verifying your email'
        email_body = 'Hi, '+user.username+' Please use the link below to activate your email \n'+absurl
        to_email = user.email
        data = {
            'email_subject': email_subject,
            'email_body': email_body,
            'to_email' : to_email,
        }

        Util.send_email(data)

        #in case to send message about email was sent 
#        context = {
#            'user_data': user_data,
#            'message' : 'verification email sent',
#        }


        return Response(user_data, status=status.HTTP_201_CREATED)

# class EmailVerify(generics.GenericAPIView): it was like this but has to be changed to let the user test it in swagger
class EmailVerify(views.APIView):
    serializer_class = EmailVerifySerializer
    renderer_classes = (UserRenderer,)

    # to let user test verification in swagger
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="descripe", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
                context = {
                    'email': 'successfully activated'
                }
            else:
                context = {
                    'email': 'email was already activated before'
                }
            return Response(context, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

'''
class RefreshTokens(generics.GenericAPIView):
    serializer_class = RefreshTokensSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
'''

class RequestPasswordRestEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordRestEmailSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            reverse_data={"uidb64":uidb64, "token":token}
            relative_link = reverse('reset-password-confirm', kwargs=reverse_data)
            absurl = "http://"+current_site+relative_link

            # preparing data to send verification email
            email_subject = 'Reset your password'
            email_body = 'Hi, Please use the link below to reset your password \n'+absurl
            to_email = user.email
            data = {
                'email_subject': email_subject,
                'email_body': email_body,
                'to_email' : to_email,
            }

            Util.send_email(data)

        context = {
            "success" : "An email was sent to you to reset your password"
        }
        return Response(context, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, requuest, uidb64, token):
        
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Invalid token, please request new one'}, status=status.HTTP_400_BAD_REQUEST)

            context = {
                "success" : True,
                "message" : "reset paasword",
                "uidb64" : uidb64,
                "token" : token,
            }
            return Response(context, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as indentifier:
            return Response({'error':'Invalid token, please request new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    renderer_classes = (UserRenderer,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        context = {
            "success" : True,
            "message" : "paasword reseted successfully",
        }
        return Response(context, status=status.HTTP_200_OK)


class LogutAPIView(generics.GenericAPIView):
    serializer_class = LogutAPIViewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthUserAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user=User.objects.get(pk=request.user.pk)
        serializer = RegisterSerializer(user)

        return Response(serializer.data)