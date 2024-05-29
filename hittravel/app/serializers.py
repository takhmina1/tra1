from rest_framework import serializers
from .models import Tour, TourRequest

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['id', 'city', 'time', 'day', 'date']

class TourRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourRequest
        fields = ['id', 'tour', 'user', 'is_approved']
