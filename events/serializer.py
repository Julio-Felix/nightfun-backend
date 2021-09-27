from rest_framework import serializers, viewsets
from .models import Events
# Serializers define the API representation.

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['title', 'establishment', 'description', 'address', 'image_url']