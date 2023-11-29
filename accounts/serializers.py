from rest_framework import serializers
from rest_framework.fields import empty
from .models import MyUser,SavedLocations
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from rest_framework.exceptions import AuthenticationFailed
from .register import register_social_user
from .google import Google


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, **kwargs):
        token = super().get_token(user)
        token['is_owner'] = user.is_owner
        token['is_admin'] = user.is_admin
        token['is_deliveryboy'] = user.is_deliveryboy
        if user.email:
            token['email'] = user.email
        if kwargs:
            token['hotel_email'] = kwargs['hotel_email']
        return token



class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    

    def validate_auth_token(self,auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again...'
            )
        if user_data['aud'] != config('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('Oops, Who are you ?...')
        

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'
        return register_social_user(
            provider = provider, user_id=user_id, email=email, name=name
        )
        



class MyuserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class MyuserPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()


class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()


class SavedLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedLocations
        fields = [
            'city',
            'district',
            'state',
            'country',
            'location'
            ]

    