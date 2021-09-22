from django.shortcuts import render
from .models import Establishment
from rest_framework import viewsets, status
from .serializer import EstablishmentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EstablishmentSerializer

