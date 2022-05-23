from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from payments.models import BankDetails
from utils.paystack_funcs import create_transfer_recipient, verify_nuban

from payments.serializers import AccountNumberSerializer, BankSerializer

# Create your views here.
class VerifyAccountNumber(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountNumberSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        nuban = serializer.validated_data["account_number"]
        bank = serializer.validated_data["bank"]
        r = verify_nuban(nuban, bank)

        return Response(r)


class CreateBankDetails(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BankSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        nuban = serializer.validated_data["account_number"]
        bank = serializer.validated_data["bank"]
        account_name = serializer.validated_data["account_name"]

        r = create_transfer_recipient(name=account_name, nuban=nuban, bank_code=bank)
        print(r)

        if r["status"] == True:
            recipient_code = r["data"]["recipient_code"]
            bank_detail = BankDetails.objects.create(
                user=request.user,
                account_name=account_name,
                account_number=nuban,
                bank=bank,
                recipient_code=recipient_code
            )
            bank_detail.save()
            return Response(r)
        else:
            return Response(r)


class ListBanks(ListAPIView):
    queryset = BankDetails.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BankSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'Bank details fetched successfully.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)