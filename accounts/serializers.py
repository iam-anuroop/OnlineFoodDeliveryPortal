from rest_framework import serializers
from .models import MyUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from rest_framework.exceptions import AuthenticationFailed
from .register import register_social_user
from .google import Google


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.phone:
            token['phone'] = user.phone
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
        






class MyuserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['phone']


class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()








    