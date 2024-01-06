from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class AuthenticateHotel(JWTAuthentication):
    def authenticate(self, request: Request):
        user, token = super().authenticate(request)
        if user and token.payload["hotel_email"]:
            return user, token.payload["hotel_email"]
        raise AuthenticationFailed("Hotel authentication failed, Please Login...")
