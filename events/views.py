from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Events
from .serializer import EventsSerializer


class EventsViewset(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventsSerializer