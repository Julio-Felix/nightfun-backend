from django.shortcuts import render
from .models import UserProfile
from rest_framework import serializers, viewsets, status
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes, action
from django.utils.crypto import get_random_string

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.filter(is_staff=False)
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def login(self, request):
        data = request.data
        code = get_random_string(9)
        try:
            user, created = UserProfile.objects.get_or_create(facebook_id=data['id'],defaults={'username':code,
                                                                                   'is_facebook_user':True,
                                                                                   'full_name':data['name'],
                                                                                   'email':data['email'],
                                                                                   'picture':data['picture']['data']['url'],
                                                                                   })
            if not created:
                return Response({'msg':'Usuário já Cadastrado, pode logar'},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'Usuário Cadastrado.'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':'Usuário Falhou no Cadastro.'},status=status.HTTP_400_BAD_REQUEST)
