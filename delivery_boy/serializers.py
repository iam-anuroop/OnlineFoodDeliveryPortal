from rest_framework import serializers
from .models import DeliveryPerson

class DeliveryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPerson
        fields = [
            'full_name',
            'location',
            'address',
            'delivery_area',
            ]

class DeliveryPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPerson
        fields = [
            'full_name',
            'location',
            'address',
            'delivery_area',
            'profile_photo',
            'id_proof'
            ]
        
class LocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


