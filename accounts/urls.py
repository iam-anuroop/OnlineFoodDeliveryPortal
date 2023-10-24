from django.urls import path
from .views import VerifyMobileNumber,GoogleAuth,VerifyPhoneOtp,RegisterWithEmail,LoginWithOtp

urlpatterns = [
    path('auth/',GoogleAuth.as_view(),name='auth'),
    path('register/',RegisterWithEmail.as_view(),name='register'),
    path('login/',LoginWithOtp.as_view(),name='login'),
    path('otpphone/',VerifyMobileNumber.as_view(),name='otpphone'),
    path('phoneverify/',VerifyPhoneOtp.as_view(),name='phoneverify'),
]
