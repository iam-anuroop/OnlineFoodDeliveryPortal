from rest_framework import serializers
from accounts.models import MyUser, UserProfile
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Shopping, ShoppingPayment, ShoppingDeliveryPerson
from hotel_panel.serializer import FoodPostSerializer
from hotel_panel.models import FoodMenu


class UserProfileSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UserProfile
        geo_field = "location"
        fields = [
            "user_address",
            "address_loc",
            "office_address",
            "office_loc",
            "alt_phone",
            "location",
        ]


class UserSerilaizer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = MyUser
        fields = ["username", "phone", "email", "userprofile"]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        userprofile_data = validated_data.pop("userprofile", None)
        if userprofile_data:
            userprofile = instance.userprofile
            for attr, value in userprofile_data.items():
                setattr(userprofile, attr, value)
            userprofile.save()
        return instance


class AddressSerializer(serializers.Serializer):
    address = serializers.CharField()
    coords = serializers.ListField(child=serializers.FloatField())


class ShoppingDeliveryPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingDeliveryPerson
        fields = "__all__"


class FoodGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodMenu
        fields = [
            "id",
            "food_name",
            "food_image",
            "food_type",
            "food_price",
            "offer_price",
            "description",
            "is_available",
            "is_veg",
        ]


class ShoppingSerializer(serializers.ModelSerializer):
    item = FoodGetSerializer()

    class Meta:
        model = Shopping
        fields = "__all__"


class AllShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingPayment
        fields = "__all__"


class ShoppingListSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField()
    hotel_image = serializers.FileField()

    class Meta:
        model = ShoppingPayment
        fields = "__all__"
