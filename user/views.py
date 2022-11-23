from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from establishment.models import Establishment
from establishment.serializer import EstablishmentSerializer
from notification.models import NotificationCenter
from .models import UserProfile, PushToken
from rest_framework import serializers, viewsets, status
from .serializer import UserSerializer, UserDataSerializer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes, action
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .utils import create_hash


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me_data(self, request):
        user = request.user
        serializer = UserDataSerializer(user)
        return Response({'user':serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_favs(self, request):
        user = request.user
        serializer = EstablishmentSerializer(user.establishments_fav.all(), many=True, context={'request': request})
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_notifications(self, request):
        user = request.user

        queryset = NotificationCenter.objects.filter(establishment=user.establishments_fav.all())

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_push_token(self, request):
        data = request.data
        try:
            pushToken = PushToken.objects.get(key=data['token'], user=request.user)
            if pushToken:
                return Response({'msg': 'Token ja Existente!'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Fluxo Inesperado!'}, status=status.HTTP_400_BAD_REQUEST)
        except PushToken.DoesNotExist:
            pushToken = PushToken.objects.create(key=data['token'], user=request.user)
            return Response({'msg': 'Token Criado com Sucesso!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': 'Criacao de Token Falhou!'}, status=status.HTTP_400_BAD_REQUEST)





    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def favorite_establishment(self, request):
        user = request.user
        establishment = Establishment.objects.get(id=request.query_params['id_establishment'])
        msg = ''
        if user.establishments_fav.filter(id=establishment.id).exists():
            msg = 'Favorito Removido com Sucesso'
            user.establishments_fav.remove(establishment)
        else:
            msg = 'Favorito Adicionado com Sucesso'
            user.establishments_fav.add(establishment)
        user.save()
        return Response({'msg': msg},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def login_facebook(self, request):
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
    def register_user(self, request):
        data = request.data
        try:
            if UserProfile.objects.filter(email=data['email']).exists():
                return Response({'msg': 'Email ja Cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)
            if UserProfile.objects.filter(username=data['email']).exists():
                return Response({'msg': 'Email ja Cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)
            user = UserProfile.objects.create(username=data['email'],
                                              email=data['email'], phone=data['phone'], full_name=data['name'])
            user.set_password(data['password'])
            names = user.full_name.split(' ', 1)
            user.first_name = names[0]
            user.last_name = names[1] if len(names) > 1 else ''
            user.save()
            return Response({'msg': 'Usuário Cadastrado.', 'token': user.auth_token.key}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': 'Usuário Falhou no Cadastro.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        data = request.data
        user = authenticate(request, username=data['username'], password=data['password'])
        try:
            return Response({'msg': 'Usuário já Cadastrado, pode logar', 'token': user.auth_token.key},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': 'Usuário Falhou no Cadastro.'}, status=status.HTTP_400_BAD_REQUEST)
