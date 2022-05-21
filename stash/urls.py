from django.urls import path

from stash.views import StashTopUpView, TransferToBankAccount, TransferToInvestmentPlan, TransferToSavingsPlan

urlpatterns = [
    path("transfer/plan/investment/", TransferToInvestmentPlan.as_view()),
    path("transfer/plan/savings/", TransferToSavingsPlan.as_view()),
    path("transfer/bank-account/", TransferToBankAccount.as_view()),
    path("topup/", StashTopUpView.as_view()),
]