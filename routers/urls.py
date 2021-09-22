from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSet
from establishment.views import EstablishmentViewSet
# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'establishment', EstablishmentViewSet)