from rest_framework import serializers, viewsets

from .models import Establishment, Schedules, SHIFTS, WEEK_DAYS, Comments
from user.models import UserProfile

# Serializers define the API representation.

class SchedulesSerializer(serializers.ModelSerializer):
    shift = serializers.SerializerMethodField(read_only=True)
    day_week =serializers.SerializerMethodField(read_only=True)

    def get_shift(self, obj):
        shift = SHIFTS[obj.sch_shift]
        return shift[1]

    def get_day_week(self, obj):
        day = WEEK_DAYS[obj.week_days - 1] # TODO: Ajeitar os Dias da semana
        return day[1]

    class Meta:
        model = Schedules
        fields = ['day_week', 'sch_begin_shift', 'sch_end_shift','shift']

class UserSerializerforEstablishment(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        depth = 1
        fields = ['full_name']
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerforEstablishment(many=False, read_only=True)
    class Meta:
        model = Comments
        depth = 1
        fields = ['text', 'linked', 'user', 'createAt']

class EstablishmentSerializer(serializers.ModelSerializer):
    sch_establishment = SchedulesSerializer(many=True, read_only=True)
    comment_establishment = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Establishment
        depth = 1
        fields = ['id', 'name', 'phone', 'description', 'address', 'sch_establishment', 'comment_establishment']
