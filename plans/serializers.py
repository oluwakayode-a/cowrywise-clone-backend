from rest_framework.serializers import ModelSerializer
from .models import UserSavingsPlan, UserInvestmentPlan, Investment, Savings


class InvestmentSerializer(ModelSerializer):
    class Meta:
        model = Investment
        fields = "__all__"

class InvestmentPlanSerializer(ModelSerializer):
    plan = InvestmentSerializer()
    class Meta:
        model = UserInvestmentPlan
        fields = "__all__"
        # exclude = ('user',)