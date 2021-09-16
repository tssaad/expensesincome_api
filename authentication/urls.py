from django.urls import path
from .views import RegisterView, EmailVerify, LoginAPIView, PasswordTokenCheckAPI,RequestPasswordRestEmail, SetNewPassword
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('email-verify/', EmailVerify.as_view(), name="email-verify"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-rest-password', RequestPasswordRestEmail.as_view(), name="request-rest-password"),
    path('reset-passoword/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name="reset-password-confirm"),
    path('paassword-reset-done', SetNewPassword.as_view(), name="paassword-reset-done"),
]



