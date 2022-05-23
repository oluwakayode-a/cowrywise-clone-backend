from .models import BankDetails
from rest_framework import serializers

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = ("id", "bank", "account_number", "account_name", "recipient_code",)
        extra_kwargs = {
            "recipient": {"read_only": True},
            "id": {"read_only": True}
        }
    
    def validate(self, attrs):
        account_number = attrs.get('account_number', '')
        if not account_number.isdigit():
            raise serializers.ValidationError("Only numbers allowed")
        return super().validate(attrs)


class AccountNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = ("bank", "account_number")
    
    def validate(self, attrs):
        account_number = attrs.get('account_number', '')
        if not account_number.isdigit():
            raise serializers.ValidationError("Only numbers allowed")
        return super().validate(attrs)