from django.urls import path
from .views import RegistrationClass,OtpVerification

urlpatterns = [
    path('registration/',RegistrationClass.as_view(),name='registration'),
    path('login/',OtpVerification.as_view(),name='login'),
]
