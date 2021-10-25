from rest_framework import serializers, viewsets
from .models import Events, Banner
# Serializers define the API representation.

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image_url', 'event']

class EventsSerializer(serializers.ModelSerializer):
    banners_events = BannerSerializer(many=True, read_only=True)
    class Meta:
        model = Events
        depth = 2
        fields = ['id', 'title', 'establishment', 'description', 'address', 'image_url', 'banners_events']