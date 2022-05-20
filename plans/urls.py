from django.urls import path
from .views import UserInvestmentPlanListCreateView, UserInvestmentPlanRUDView

urlpatterns = [
    path('investments/', UserInvestmentPlanListCreateView.as_view()),
    path("investments/<int:id>/", UserInvestmentPlanRUDView.as_view()),
]