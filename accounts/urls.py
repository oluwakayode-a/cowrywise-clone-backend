from django.urls import path
from django.contrib.auth.views import PasswordResetCompleteView

urlpatterns = [
    path("register/", PasswordResetCompleteView.as_view())
]