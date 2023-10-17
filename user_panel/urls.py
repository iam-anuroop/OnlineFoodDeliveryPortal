from django.urls import path
from .views import ProfileManage

urlpatterns = [
    path('profile/',ProfileManage.as_view(),name='profile'),
]
