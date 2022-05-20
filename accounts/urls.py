from django.urls import path
from accounts.views import SendOTPRegisterView, UserRegisterView, VerifyOTPRegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("send-otp-register/", SendOTPRegisterView.as_view()),
    path("verify-otp-register/", VerifyOTPRegisterView.as_view()),
    path("register/", UserRegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]