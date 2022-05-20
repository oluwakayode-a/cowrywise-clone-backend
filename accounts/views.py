from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accounts.serializers import LoginSerializer, OTPSerializer, SubmitEmailSerializer, UserSerializer
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

        return Response(serializer.data, status=status.HTTP_200_OK)


