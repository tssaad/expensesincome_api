from typing import Generic
from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions


from .serializers import IcomeSerializer
from .models import Income
from .permissions import IsOwner


class IncomeListAPIView(ListCreateAPIView):
    serializer_class = IcomeSerializer
    queryset=Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user) # to override the save method so the action will be saved under the owner which is the current owner

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user) # to retrieve only expeses were made by the owner


class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = IcomeSerializer
    queryset=Income.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user) # to retrieve only expeses were made by the owner

