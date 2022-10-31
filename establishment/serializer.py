from math import radians, cos, atan2, sin, sqrt

from rest_framework import serializers, viewsets

from .models import Establishment, Schedules, SHIFTS, WEEK_DAYS, Comments
from user.models import UserProfile

# Serializers define the API representation.

def calculate_distance(latitude1,longitude1,latitude2,longitude2):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(latitude1)
    lon1 = radians(longitude1)
    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

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
        fields = ['full_name', 'picture']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerforEstablishment(many=False, read_only=True)
    class Meta:
        model = Comments
        depth = 1
        fields = ['text', 'linked', 'user', 'createAt']

class EstablishmentSerializer(serializers.ModelSerializer):
    sch_establishment = SchedulesSerializer(many=True, read_only=True)
    comment_establishment = CommentSerializer(many=True, read_only=True)
    distance = serializers.SerializerMethodField()
    is_fav = serializers.SerializerMethodField()

    def get_is_fav(self, obj):
        return self.context['request'].user.establishments_fav.filter(id=obj.id).exists()


    def get_distance(self, obj):
        distance = None
        if self.context['coords'] != None and self.context['coords'] != [] and 'lat' in self.context['coords']:
            coords = self.context['coords']
            distance = calculate_distance(obj.lat, obj.long,
                                          float(coords['lat']), float(coords['long']))
        return distance

    class Meta:
        model = Establishment
        depth = 1
        fields = ['id', 'name', 'phone', 'distance','lat', 'long', 'description', 'address', 'is_fav',
                  'logo', 'sch_establishment', 'comment_establishment']


