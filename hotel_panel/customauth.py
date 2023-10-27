from typing import Optional, Tuple
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import Token
from .models import HotelOwner,HotelsAccount
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class AuthenticateHotel(JWTAuthentication):
    def authenticate(self, request: Request):
        user,token = super().authenticate(request)
        print(token.payload['hotel_email'],'authhhhhhhhhhhhhhhhhhhhh')
        if user and token.payload['hotel_email']:
            return user,None
        raise AuthenticationFailed('Hotel authentication failed, Please Login...')