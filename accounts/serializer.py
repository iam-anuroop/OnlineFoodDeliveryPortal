from rest_framework import serializers
from .models import MyUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken



class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.phone:
            token['phone'] = user.phone
        return token



class MyuserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['phone']


class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()








    