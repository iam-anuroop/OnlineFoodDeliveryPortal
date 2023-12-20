from rest_framework import serializers
from accounts.models import MyUser, UserProfile
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserProfileSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UserProfile
        geo_field = "location"
        fields = ["user_address","address_loc", "office_address","office_loc", "alt_phone", "location"]


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

