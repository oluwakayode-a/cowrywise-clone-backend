from django.db.models import query
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import InvestmentPlanSerializer, InvestmentSerializer
from .models import Investment, User, UserInvestmentPlan


# Create your views here.
class Investments(ListCreateAPIView):
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all()

class UserInvestmentPlan(ListCreateAPIView):
    serializer_class = InvestmentPlanSerializer
    queryset = UserInvestmentPlan.objects.all()
