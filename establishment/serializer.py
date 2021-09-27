from rest_framework import serializers, viewsets
from .models import Establishment
# Serializers define the API representation.

class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        depth = 1
        fields = ['name', 'description', 'address', 'phone']
