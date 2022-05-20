from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed, PermissionDenied
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User

class SubmitEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = "__all__"
    
    def validate(self, attrs):
        email = attrs.get("email", "")
        _check_email = User.objects.filter(email=email)
        if _check_email.exists():
            raise ValidationError("User with this email exists. Please sign in or verify your account")
        return super().validate(attrs)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(max_length=68,
                                     min_length=5,
                                     write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, user):
        user = User.objects.get(email=user['email'])
        return {
            'access' : user.tokens['access'],
            'refresh' : user.tokens['refresh']
        }
    class Meta:
        model = User
        fields = ["email", "password", "tokens"]
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            raise AuthenticationFailed("Incorrect email or password.")
        
        if not user.is_active:
            raise PermissionDenied("Your account has been deactivated. Please contact admin.")
        return {
            "email" : user.email
        }

class OTPSerializer(serializers.Serializer):
    token = serializers.IntegerField()

    class Meta:
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "phone_number"]
    
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data["phone_number"]
        )
        user.set_password(validated_data["password"])
        user.save()

        return user
    
    
    def validate(self, attrs):
        email = attrs.get("email", "")
        phone_number = attrs.get("phone_number", "")

        _check_email = User.objects.filter(email=email)
        _check_phone_number = User.objects.filter(phone_number=phone_number)

        if _check_email.exists():
            raise ValidationError("User with this email exists. Please sign in or verify your account")
        
        if _check_phone_number.exists():
            raise ValidationError("User with this phone number exists.")
        return super().validate(attrs)