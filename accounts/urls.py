from django.urls import path
from accounts.views import NextofKinUpdateView, SecurityPrefsUpdateView, SendOTPRegisterView, UserRegisterView, UpdateProfileView, SecurityPrefsUpdateView, ChangePasswordView, SetNewPasswordView, VerifyOTPRegisterView, LoginView, PasswordResetView, PasswordResetConfirmView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("send-otp-register/", SendOTPRegisterView.as_view()),
    path("verify-otp-register/", VerifyOTPRegisterView.as_view()),
    path("register/", UserRegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("password-reset/", PasswordResetView.as_view()),
    path("password-reset-confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("set-new-password/", SetNewPasswordView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("update-profile/", UpdateProfileView.as_view()),
    path("update-security-prefs/", SecurityPrefsUpdateView.as_view()),
    path("update-next-of-kin/", NextofKinUpdateView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
