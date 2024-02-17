# serializers.py
from rest_framework import serializers
from .models import PetMeetUp, PetType, PetBreed


class PetMeetUpSerializer(serializers.ModelSerializer):
    pet_type = serializers.CharField()
    pet_breed = serializers.CharField()

    class Meta:
        model = PetMeetUp
        fields = '__all__'
