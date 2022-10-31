import datetime
import random
import string

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Events, Banner, Ticket
from .serializer import EventsSerializer, BannerSerializer


class EventsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Events.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventsSerializer

    @action(detail=False, methods=['GET'])
    def generate_ticket(self, request, pk=None):
        user = request.user
        event = Events.objects.get(id=request.query_params['event_id'])
        while True:
            length = 9
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not Ticket.objects.filter(user=user, code=str(ran), event=event).exists():
                dateExpiration = datetime.datetime.now() + datetime.timedelta(hours=12)
                Ticket.objects.create(user=user, code=str(ran), event=event,
                                      expiration_date=dateExpiration)
                break
        return Response({'code': str(ran), 'expirationDate': dateExpiration.strftime('%d/%m/%Y %H:%M')},
                        status=status.HTTP_200_OK)

class BannersViewset(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BannerSerializer