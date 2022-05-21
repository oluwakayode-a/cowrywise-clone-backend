from django.shortcuts import render
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from plans.models import Savings, UserInvestmentPlan

from stash.serializers import StashSerializer, TransferStashSerializer
from utils.paystack_funcs import transfer, verify_transaction
from .models import Stash
from accounts.models import User

# Create your views here.
class StashTopUpView(GenericAPIView):
    """
    Callback URL on Payment Successful. Amount.
    """
    serializer_class = StashSerializer
    authentication_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        reference = serializer.validated_data["reference"]

        tx = verify_transaction(reference)
        if tx:
            amount = serializer.validated_data["amount"]

            stash = Stash.objects.get(user=request.user)
            stash.balance = F("balance") + int(amount)
            stash.save()

            response = {
                'status' : 'success',
                'code' : status.HTTP_200_OK,
                'message' : 'Stash top up successfull',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'status' : "pending",
                "code" : "",
                "message" : "Transaction has not been verified",
                "data" : []
            }
            return Response(response, status=status.HTTP_100_CONTINUE)


class TransferToInvestmentPlan(GenericAPIView):
    """
    Transfer from Stash Balance to Investment Plan Balance
    """
    serializer_class = TransferStashSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = int(serializer.validated_data["amount"])
        plan_id = int(serializer.validated_data["plan_id"])

        stash = Stash.objects.get(user=request.user)
        plan = UserInvestmentPlan.objects.filter(plan_id)

        if plan.exists():
            if stash.balance < amount:
                # Return failed
                response = {
                    'status' : 'error',
                    'code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Insufficient funds in stash',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Top up plan.
                plan.balance = F("balance") + amount
                stash.balance = F("balance") - amount

                plan.save()
                stash.save()

                response = {
                    'status' : 'success',
                    'code' : status.HTTP_200_OK,
                    'message' : 'Transfer successful',
                    'data': serializer.data
                }

                return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error" : "Plan does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    

class TransferToSavingsPlan(GenericAPIView):
    """
    Transfer from Stash Balance to Savings Plan Balance
    """
    serializer_class = TransferStashSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = int(serializer.validated_data["amount"])
        plan_id = int(serializer.validated_data["plan_id"])

        stash = Stash.objects.get(user=request.user)
        plan = Savings.objects.get(plan_id)
        if plan.exists():
            if stash.balance < amount:
                # Return failed
                response = {
                    'status' : 'error',
                    'code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Insufficient funds in stash',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Top up plan.
                plan.balance = F("balance") + amount
                stash.balance = F("balance") - amount

                plan.save()
                stash.save()

                response = {
                    'status' : 'success',
                    'code' : status.HTTP_200_OK,
                    'message' : 'Transfer successful',
                    'data': serializer.data
                }

                return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error" : "Plan does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class TransferToBankAccount(GenericAPIView):
    serializer_class = TransferStashSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = int(serializer.validated_data["amount"])
        stash = Stash.objects.get(user=request.user)

        if stash.balance < amount:
            # Return failed
            response = {
                'status' : 'error',
                'code' : status.HTTP_400_BAD_REQUEST,
                'message' : 'Insufficient funds in stash',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = transfer(amount, stash)
            if response:
                stash.balance = F("balance") - amount
                stash.save()

                response = {
                    'status' : 'success',
                    'code' : status.HTTP_200_OK,
                    'message' : 'Transfer successful',
                    'data': serializer.data
                }

                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"error" : "Error occurred."}, status=status.HTTP_400_BAD_REQUEST)




