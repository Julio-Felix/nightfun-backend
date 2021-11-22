from django.shortcuts import render
from .models import UserProfile
from rest_framework import serializers, viewsets, status
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes, action
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


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
                user.picture=data['picture']['data']['url']
                user.save()
                return Response({'msg': 'Usuário já Cadastrado, pode logar', 'token': user.auth_token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Usuário Cadastrado.', 'token': user.auth_token.key}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': 'Usuário Falhou no Cadastro.'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def loginwithoutFacebook(self, request):
        data = request.data
        user = authenticate(request, username=data['username'], password=data['password'])
        try:
            return Response({'msg': 'Usuário já Cadastrado, pode logar', 'token': user.auth_token.key},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': 'Usuário Falhou no Cadastro.'}, status=status.HTTP_400_BAD_REQUEST)
