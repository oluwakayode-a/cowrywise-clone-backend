from rest_framework import serializers
from .models import UserSavingsPlan, UserInvestmentPlan, Investment, Savings


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = "__all__"

class InvestmentPlanSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)
    class Meta:
        model = UserInvestmentPlan
        fields = ("id", "plan", "amount", "balance",)
        extra_kwargs={"balance" : {"read_only" : True}}
    
    def create(self, validated_data):
        validated_data.pop("amount", None)
        return super().create(validated_data)


class InvestmentPlanRUDSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)
    class Meta:
        model = UserInvestmentPlan
        fields = ("id", "plan", "amount", "balance",)
        extra_kwargs={"balance" : {"read_only" : True}, "plan" : {"read_only" : True}}
    
    def update(self, instance, validated_data):
        validated_data.pop("amount", None)
        return super().update(instance, validated_data)
