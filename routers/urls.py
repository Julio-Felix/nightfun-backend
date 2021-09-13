from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
# Create a router and register our viewsets with it.
userRouter = DefaultRouter()

userRouter.register(r'users', UserViewSet)