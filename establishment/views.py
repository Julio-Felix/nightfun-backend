import datetime

from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
import string
import random
from .models import Establishment, Comments, Ticket
from rest_framework import viewsets, status
from .serializer import EstablishmentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EstablishmentSerializer

    @action(detail=False, methods=['POST'])
    def add_comment(self, request, pk=None):
        user = request.user
        data = request.data
        data['user'] = user
        data['establishment'] = Establishment.objects.get(id=data['establishment'])
        comment = Comments.objects.create(**data)
        return Response({'status': 'Comment Added'})

    @action(detail=False, methods=['GET'])
    def generate_ticket(self, request, pk=None):
        user = request.user
        establishment = Establishment.objects.get(id=request.query_params['establishment_id'])
        while True:
            length = 9
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not Ticket.objects.filter(user=user, code=str(ran), establishment=establishment).exists():
                dateExpiration = datetime.datetime.now() + datetime.timedelta(hours=12)
                Ticket.objects.create(user=user, code=str(ran), establishment=establishment,
                                      expiration_date=dateExpiration)
                break
        return Response({'code': str(ran), 'expirationDate': dateExpiration.strftime('%d/%m/%Y %H:%M')}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['GET'])
    def rank_establishment(self, request, pk=None):
        establishments = Establishment.objects.all()
        data = []
        try:
            for establishment in establishments:
                likeds = establishment.comment_establishment.filter(linked=True).count()
                data.append({'name': establishment.name, 'liked': likeds})
            data.sort(key=lambda x: x['liked'],reverse=True)
            return Response({'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': "Desculpa Encontramos Problemas no Processamneot"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)