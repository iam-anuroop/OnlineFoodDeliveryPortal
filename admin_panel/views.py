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
from drf_yasg.utils import swagger_auto_schema
from accounts.utils import send_email


@permission_classes([IsAdminUser,IsAuthenticated])
class AdminHotelManage(APIView):
    
    @swagger_auto_schema(
        tags=["Admin panel"],
        operation_description="Approving Hotels By Admin",
        responses={
            200:"Okay",
            400:"errors"
        }
    )
    def post(self,request):
        hotel_email = request.data.get('hotel_email')
        try:
            hotel = HotelsAccount.objects.get(email = hotel_email)
            hotel.is_approved = True
            hotel.save()
            subject = "Buisiness Approved"
            message = "Your Account has been verified and approved successfully"
            send_email(email=hotel_email,subject=subject,message=message)
            return Response({'msg':'Successfully done'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':'no hotel with this mail'},status=status.HTTP_400_BAD_REQUEST)
    


    @swagger_auto_schema(
        tags=["Admin panel"],
        operation_description="Listing All Unapproved Hotels",
        responses={
            200:HotelAccountSeriallizer,
            400:"errors"
        }
    )
    def get(self,request):
        hotels = HotelsAccount.objects.filter(
            Q(is_active=True) & 
            Q(is_approved = False)
            )
        try:
            serializer = HotelAccountSeriallizer(hotels,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':"Error While Serializing"},status=status.HTTP_400_BAD_REQUEST)





@permission_classes([IsAdminUser,IsAuthenticated])
class AdminPanelApprovedHotels(APIView):

    @swagger_auto_schema(
        tags=["Admin panel"],
        operation_description="Listing All Approved Hotels",
        responses={
            200:HotelAccountSeriallizer,
            400:"errors"
        }
    )
    def get(self,request):
        hotels = HotelsAccount.objects.filter(
            Q(is_active=True) & 
            Q(is_approved = True)
            )
        try:
            count_hotels = len(hotels)
            pagination = CustomUserListPagination()
            count_pages = [i for i in range(1,count_hotels // pagination.page_size +1)]
            result_page = pagination.paginate_queryset(hotels,request)
            serializer = HotelAccountSeriallizer(result_page,many=True)
            return Response({'data':serializer.data,'page_count':count_pages},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":"Somthing Wrong while serialising"},status=status.HTTP_400_BAD_REQUEST)




@permission_classes([IsAdminUser,IsAuthenticated])
class AdminPanelUsersList(APIView):

    @swagger_auto_schema(
        tags=["Admin panel"],
        operation_description="Listing All Users",
        responses={
            200:UserSerilaizer,
            400:"errors"
        }
    )
    def get(self,request):
        users = MyUser.objects.all()
        try:
            count_users = len(users)
            pagination = CustomUserListPagination()
            count_pages = count_users // pagination.page_size
            result_page = pagination.paginate_queryset(users,request)
            serializer = UserSerilaizer(result_page,many=True)
            return Response({'data':serializer.data,'page_count':count_pages},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'Errors While Serializing'},status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
