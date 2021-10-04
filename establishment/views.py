from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

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

    @action(detail=False, methods=['POST'])
    def add_comment(self, request, pk=None):
        user = request.user
        data = request.data
        data['user'] = user
        data['establishment'] = Establishment.objects.get(id=data['establishment'])
        comment = Comments.objects.create(**data)
        return Response({'status': 'Comment Added'})