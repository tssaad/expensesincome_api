from typing import Generic
from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions


from .serializers import ExpensesSerializer, ExpensesSerializer
from .models import Expenses
from .permissions import IsOwner

from authentication.models import User

class ExpensesListAPIView(ListCreateAPIView):
    serializer_class = ExpensesSerializer
    queryset=Expenses.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user) # to override the save method so the action will be saved under the owner which is the current owner

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user) # to retrieve only expeses were made by the owner


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpensesSerializer
    queryset=Expenses.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user) # to retrieve only expeses were made by the owner

