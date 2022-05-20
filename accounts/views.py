from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.models import NextofKin, Profile, Security, User


from accounts.serializers import ChangePasswordSerializer, LoginSerializer, NextofKinSerializer, OTPSerializer, PasswordResetSerializer, ProfileSerializer, SecuritySerializer, SetNewPasswordSerializer, SubmitEmailSerializer, UserSerializer
from utils.send_email import send_email
from utils.otp import generate_otp, verify_otp

class SendOTPRegisterView(GenericAPIView):
    """
    Get User Email, and send an OTP to the User.
    """
    serializer_class = SubmitEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        
        try:
            otp = generate_otp()
            send_email(email_to=email, title="OTP to complete your signup", content=otp)
            
            return Response({"success" : "Please check your email for OTP", "email" : email}, status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            return Response({"error" : "Error occured. Please try again."}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPRegisterView(GenericAPIView):
    """
    Verify that the OTP is valid, and redirect to the login page.
    """
    serializer_class = OTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]

        verified = verify_otp(token)
        if verified:
            return Response({"success" : "OTP Verified. Redirect to sign up page."}, status=status.HTTP_200_OK)
        else:
            return Response({"error" : "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"success" : "User registered successfully."}, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {
            'status' : 'success',
            'message' : "Login successful.",
            "data" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data["email"])
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

        token = PasswordResetTokenGenerator().make_token(user)
        redirect_url = request.data.get("redirect_url")

        url = f"http://{get_current_site(request).domain}{reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token' : token})}?redirect_url={redirect_url}"
        
        send_email(email_to=user.email, title="Reset Password", content=f"Hi, {user.username}, use the link below to reset your password. \n {url}")
        if send_email: # Email successfully sent
            response = {
                'status' : 'success',
                'message' : "We have sent you a link to reset your password.",
                "data" : []
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'status' : 'error',
                'message' : "Error Occured",
                "data" : []
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetConfirmView(APIView):
    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url')

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                if redirect_url:
                    return redirect(f"{redirect_url}?token_valid=False")
                # return Response({"error" : "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
        except UnicodeDecodeError:
            # return Response({"error" : "Token Error"}, status=status.HTTP_400_BAD_REQUEST)
            return redirect(f"{redirect_url}?token_valid=False")
        
        # return Response({"success" : True}, status=status.HTTP_200_OK)
        return redirect(f"{redirect_url}?token_valid=True&?token={token}&?uidb64={uidb64}")


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status' : 'success',
            'message' : "Password Reset Succesful",
            "data" : []
        }
        return Response(response, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(UpdateAPIView):
    """
    Enpoint for updating User Profile
    """
    model = Profile
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self, queryset=None):
        obj = Profile.objects.get(user=self.request.user)
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=self.object)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'Profile updated successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class SecurityPrefsUpdateView(UpdateAPIView):
    """
    Endpoint for updating user security preferences
    """
    model = Security
    serializer_class = SecuritySerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        obj = Security.objects.get(user=self.request.user)
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=self.object)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'Profile updated successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class NextofKinUpdateView(UpdateAPIView):
    """
    Endpoint for updating user security preferences
    """
    model = NextofKin
    serializer_class = NextofKinSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        obj = NextofKin.objects.get(user=self.request.user)
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=self.object)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'Profile updated successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

        

