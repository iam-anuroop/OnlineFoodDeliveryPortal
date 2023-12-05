from rest_framework import serializers
from accounts.models import MyUser, UserProfile
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserProfileSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UserProfile
        geo_field = "location"
        fields = ["user_address", "office_address", "alt_phone", "location"]


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

    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.email = validated_data.get('email', instance.email)

    #     # Update fields of userprofile using the nested serializer
    #     userprofile_data = validated_data.get('userprofile')
    #     if userprofile_data:
    #         userprofile = instance.userprofile
    #         userprofile.user_address = userprofile_data.get('user_address', userprofile.user_address)
    #         userprofile.alt_phone = userprofile_data.get('alt_phone', userprofile.alt_phone)

    #         # Check if "geometry" and "coordinates" are present in the userprofile_data
    #         if 'geometry' in userprofile_data and 'coordinates' in userprofile_data['geometry']:
    #             userprofile.location = {
    #                 "type": "Point",
    #                 "coordinates": userprofile_data['geometry']['coordinates']
    #             }
    #         userprofile.save()
    #         instance.save()
    #     return super().update(instance, validated_data)
