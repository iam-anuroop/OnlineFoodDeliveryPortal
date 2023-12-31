from rest_framework import serializers
from .models import HotelsAccount, HotelOwner, FoodMenu


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOwner
        fields = [
            "first_name",
            "last_name",
            "email",
            "contact",
            "id_proof",
            "id_number",
        ]


class EmailSeriaizer(serializers.Serializer):
    email = serializers.EmailField()


class HotelAccountSeriallizer(serializers.ModelSerializer):
    owner = OwnerSerializer()

    class Meta:
        model = HotelsAccount
        exclude = ["is_active"]


class FoodPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodMenu
        fields = [
            "id",
            "food_name",
            # "food_image",
            "food_type",
            "food_price",
            "offer_price",
            "description",
            "is_available",
            "is_veg",
        ]


class FoodGetSerializer(serializers.ModelSerializer):
    hotel = HotelAccountSeriallizer()

    class Meta:
        model = FoodMenu
        fields = [
            "id",
            "hotel",
            "food_name",
            "food_image",
            "food_type",
            "food_price",
            "offer_price",
            "description",
            "is_available",
            "is_veg",
        ]


class FoodmenuSerializer(serializers.ModelSerializer):
    hotel = HotelAccountSeriallizer()

    class Meta:
        model = FoodMenu
        exclude = ["is_veg"]
