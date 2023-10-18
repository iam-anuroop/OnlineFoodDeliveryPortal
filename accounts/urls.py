from django.urls import path
from .views import RegistrationClass,OtpVerification,GoogleAuth

urlpatterns = [
    path('registration/',RegistrationClass.as_view(),name='registration'),
    path('login/',OtpVerification.as_view(),name='login'),
    path('auth/',GoogleAuth.as_view(),name='auth')
]
