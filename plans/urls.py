from django.urls import path
from .views import UserInvestmentPlanListCreateView, UserInvestmentPlanRUDView, SavingsListCreateView, SavingsRUDView

urlpatterns = [
    path('investments/', UserInvestmentPlanListCreateView.as_view()),
    path("investments/<int:id>/", UserInvestmentPlanRUDView.as_view()),
    path('savings/', SavingsListCreateView.as_view()),
    path("savings/<int:id>/", SavingsRUDView.as_view()),
]