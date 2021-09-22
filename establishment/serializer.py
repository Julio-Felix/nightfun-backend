from rest_framework import serializers, viewsets
from .models import Establishment
# Serializers define the API representation.
class EstablishmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Establishment
        fields = ['name' ]
