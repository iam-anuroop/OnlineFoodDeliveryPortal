from rest_framework import serializers
from .models import HotelsAccount,HotelOwner



class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOwner
        fields = ['first_name','last_name','email','contact','id_proof','id_number']


class HotelAccountSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = HotelsAccount
        exclude = ['owner','is_approved','rating','is_active']



class EmailSeriaizer(serializers.Serializer):
    email = serializers.EmailField()

