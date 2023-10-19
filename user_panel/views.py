# from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import authenticate
from .serializers import UserSerilaizer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import MyUser,UserProfile
from ipware import get_client_ip
import json, urllib
from decouple import config




class UserCurrentLocation(APIView):
    def post(self,request):
        client_ip, is_routable = get_client_ip(request)
        # if client_ip is None:
        #     client_ip='0.0.0.0'
        if is_routable:
            ip_type = 'public'
        else:
            ip_type = 'private'
        ip_address = "218.53.14.236"
        auth = config('FIND_IP_AUTH')
        url = "https://api.ipfind.com/?auth="+auth+"&ip="+ip_address
        resp = urllib.request.urlopen(url)
        data1 = json.loads(resp.read())
        data1['client_ip'] = client_ip
        data1['ip_type'] = ip_type
        return Response(data1)



@permission_classes([IsAuthenticated])
class ProfileManage(APIView):
    def get(self,request):
        currentuser = request.user
        user = MyUser.objects.get(id=currentuser.id)
        serializer = UserSerilaizer(user)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    
    def patch(self, request):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile:
                serializer = UserSerilaizer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            UserProfile.objects.create(user=user)
            serializer = UserSerilaizer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request):
        user = request.user
        user.delete()
        return Response({'msg':'Account deleted...'},status=status.HTTP_200_OK)

# Create your views here.
