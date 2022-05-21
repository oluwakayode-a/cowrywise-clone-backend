from rest_framework import serializers
from .models import Savings, UserInvestmentPlan, Investment, Savings


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = "__all__"


class InvestmentPlanSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserInvestmentPlan
        fields = ("id", "plan", "amount", "balance",)
        extra_kwargs = {"balance": {"read_only": True}}

    def create(self, validated_data):
        validated_data.pop("amount", None)
        return super().create(validated_data)


class InvestmentPlanRUDSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserInvestmentPlan
        fields = ("id", "plan", "amount", "balance",)
        extra_kwargs = {"balance": {"read_only": True},
                        "plan": {"read_only": True}}

    def update(self, instance, validated_data):
        validated_data.pop("amount", None)
        return super().update(instance, validated_data)


class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savings
        fields = ("id", "amount", "savings_type", "balance", "frequency")
        extra_kwargs = {
            "balance": {"read_only": True},
            "id": {"read_only": True}
        }


class SavingsRUDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Savings
        fields = ("id", "amount", "balance",)
        extra_kwargs = {
            "balance": {"read_only": True}, 
            "savings_type": {"read_only": True}, 
            "id": {"read_only": True}
        }
