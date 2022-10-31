from rest_framework import serializers

from notification.models import NotificationCenter


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NotificationCenter
        fields = '__all__'
