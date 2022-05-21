from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvestmentPlanRUDSerializer, InvestmentPlanSerializer, SavingsSerializer, SavingsRUDSerializer
from .models import User, UserInvestmentPlan, Savings


# Create your views here.
class UserInvestmentPlanListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = InvestmentPlanSerializer
    queryset = UserInvestmentPlan.objects.all()
    
    def get_object(self):
        plan = UserInvestmentPlan.objects.get(user=self.request.user)
        return plan
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save(user=request.user, balance=serializer.validated_data["amount"])

        response = {
            'status' : 'success',
            'code' : status.HTTP_201_CREATED,
            'message' : 'Investment plan created successfully.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
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
            'message' : 'User investment plans fetched successfully.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class UserInvestmentPlanRUDView(RetrieveUpdateDestroyAPIView):
    queryset = UserInvestmentPlan.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = InvestmentPlanRUDSerializer
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)

        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'User investment plan fetched successfully.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=self.object)
        serializer.is_valid(raise_exception=True)
        
        # Increment balance
        balance = self.object.balance + serializer.validated_data["amount"]
        serializer.save(balance=balance)
        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'User investment plan updated successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'User investment plan deleted successfully',
            'data': []
        }
        return Response(response, status=status.HTTP_200_OK)


class SavingsListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SavingsSerializer
    queryset = Savings.objects.all()
    
    def get_object(self):
        plan = Savings.objects.get(user=self.request.user)
        return plan
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save(user=request.user, balance=serializer.validated_data["amount"])

        response = {
            'status' : 'success',
            'code' : status.HTTP_201_CREATED,
            'message' : 'Savings plan created successfully.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
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
            'message' : 'User Savings plans fetched successfully.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class SavingsRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Savings.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = SavingsRUDSerializer
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)

        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'User Savings plan fetched successfully.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """
        This can be automated if it's a periodic option, via Celery periodic tasks.
        """
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=self.object)
        serializer.is_valid(raise_exception=True)
        
        # Increment balance
        balance = self.object.balance + serializer.validated_data["amount"]
        serializer.save(balance=balance)
        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'User Savings plan updated successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response = {
            'status' : 'success',
            'code' : status.HTTP_200_OK,
            'message' : 'User Savings plan deleted successfully',
            'data': []
        }
        return Response(response, status=status.HTTP_200_OK)

