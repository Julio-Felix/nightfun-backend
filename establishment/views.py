import datetime

from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
import string
import random
from .models import Establishment, Comments
from rest_framework import viewsets, status
from .serializer import EstablishmentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EstablishmentSerializer

    def get_serializer_context(self):
        context = super(EstablishmentViewSet, self).get_serializer_context()
        context.update({"coords": self.request.query_params})
        return context

    @action(detail=False, methods=['POST'])
    def add_comment(self, request, pk=None):
        user = request.user
        data = request.data
        data['user'] = user
        data['establishment'] = Establishment.objects.get(id=data['establishment'])
        comment = Comments.objects.create(**data)
        return Response({'status': 'Comment Added'})



    @action(detail=False, methods=['GET'])
    def rank_establishment(self, request, pk=None):
        establishments = Establishment.objects.all()
        data = []
        try:
            for establishment in establishments:
                likeds = establishment.comment_establishment.filter(linked=True).count()
                data.append({'name': establishment.name, 'liked': likeds})
            data.sort(key=lambda x: x['liked'],reverse=True)
            return Response({'data': data[0:9]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': "Desculpa Encontramos Problemas no Processamneot"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)