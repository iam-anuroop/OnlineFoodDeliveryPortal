from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import permission_classes
from hotel_panel.models import HotelsAccount
from accounts.models import UserProfile , MyUser
from user_panel.serializers import UserSerilaizer
from hotel_panel.serializer import HotelAccountSeriallizer
from django.db.models import Q
from .pagination import CustomUserListPagination
# from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination



@permission_classes([IsAdminUser,IsAuthenticated])
class AdminHotelManage(APIView):
    # pagination_class = CustomUserListPagination

    def post(self,request):
        hotel_email = request.data.get('hotel_email')
        try:
            hotel = HotelsAccount.objects.get(email = hotel_email)
            hotel.is_approved = True
            hotel.save()
        except Exception as e:
            return Response({'msg':'no hotel with this mail'},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        data = request.data.get('data')
        print(data)
        if data == 'users':
            res = self.get_users(request)
        if data == 'hotels':
            res = self.get_hotels()
        if data == 'unapproved_hotels':
            res = self.get_unApprovedHotels()
        if res['status']=='ok':
            return Response(res,status=status.HTTP_200_OK)
        return Response(res,status=status.HTTP_400_BAD_REQUEST) 
    
    def get_users(self,request):
        users = MyUser.objects.all()
        try:
            count_users = len(users)
            pagination = CustomUserListPagination()
            count_pages = count_users // pagination.page_size
            result_page = pagination.paginate_queryset(users,request)
            serializer = UserSerilaizer(result_page,many=True)
            return {'data':serializer.data,'page_count':count_pages,'status':'ok'}
        except Exception as e:
            print(e)
            return {'data':"Somthing Wrong while serialising",'status':'error'}
        
    def get_hotels(self):
        hotels = HotelsAccount.objects.filter(
            Q(is_active=True) & 
            Q(is_approved = True)
            )
        try:
            serializer = HotelAccountSeriallizer(hotels,many=True)
            return {'data':serializer.data,'status':'ok'}
        except Exception as e:
            return {'data':"Somthing Wrong while serialising",'status':'error'}
        
    def get_unApprovedHotels(self):
        hotels = HotelsAccount.objects.filter(
            Q(is_active=True) & 
            Q(is_approved = False)
            )
        try:
            serializer = HotelAccountSeriallizer(hotels,many=True)
            return {'data':serializer.data,'status':'ok'}
        except Exception as e:
            return {'data':"Somthing Wrong while serialising",'status':'error'}



# Create your views here.
