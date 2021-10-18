from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Events, Banner
from .serializer import EventsSerializer, BannerSerializer


class EventsViewset(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventsSerializer

class BannersViewset(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BannerSerializer