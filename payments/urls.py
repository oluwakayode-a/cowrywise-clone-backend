from django.urls import path

from payments.views import CreateBankDetails, ListBanks, VerifyAccountNumber

urlpatterns = [
    path("verify-nuban/", VerifyAccountNumber.as_view()),
    path("bank-details/", ListBanks.as_view()),
    path("bank-details/add/", CreateBankDetails.as_view()),
]