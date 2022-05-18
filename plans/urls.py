from django.urls import path
from .views import Investments, UserInvestmentPlan

urlpatterns = [
    path('inv-plan', UserInvestmentPlan.as_view()),
    path('investments', Investments.as_view())
]