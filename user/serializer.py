from rest_framework import serializers, viewsets
from .models import UserProfile
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'is_facebook_user']

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['facebook_id', 'password']