# from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import authenticate
from .serializers import UserSerilaizer,UserProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import MyUser





@permission_classes([IsAuthenticated])
class ProfileManage(APIView):
    def get(self,request):
        currentuser = request.user
        user = MyUser.objects.get(id=currentuser.id)
        # user = request.user
        serializer = UserSerilaizer(user)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request):
        user = request.user
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
