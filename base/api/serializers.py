from rest_framework import serializers
from base.models import Room

class RoomSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d")  # Define the format you want
    created = serializers.DateTimeField(format="%Y-%m-%d")  # Define the format you want

    class Meta:
        model = Room
        fields = '__all__'
