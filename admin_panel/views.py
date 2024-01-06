from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import permission_classes
from hotel_panel.models import HotelsAccount
from accounts.models import MyUser
from user_panel.serializers import UserSerilaizer
from hotel_panel.serializer import HotelAccountSeriallizer
from django.db.models import Q
from .pagination import CustomUserListPagination
from drf_yasg.utils import swagger_auto_schema
from accounts.utils import send_email
from delivery_boy.models import DeliveryPerson
from delivery_boy.serializers import DeliveryPersonSerializer


@permission_classes([IsAdminUser, IsAuthenticated])
class AdminHotelManage(APIView):
    @swagger_auto_schema(
        tags=["Admin panel"],
        operation_description="Approving Hotels By Admin",
        responses={200: "Okay", 400: "errors"},
    )
    def post(self, request):
        hotel_email = request.data.get("hotel_email")
        try:
            hotel = HotelsAccount.objects.get(email=hotel_email)
            hotel.is_approved = True
            hotel.save()
            subject = "Buisiness Approved"
            message = "Your Account has been verified and approved successfully"
            send_email(email=hotel_email, subject=subject, message=message)
            return Response({"msg": "Successfully done"}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"msg": "no hotel with this mail"}, status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        tags=["Admin panel"],
        operation_description="Listing All Unapproved Hotels",
        responses={200: HotelAccountSeriallizer, 400: "errors"},
    )
    def get(self, request):
        hotels = HotelsAccount.objects.filter(Q(is_active=True) & Q(is_approved=False))
        try:
            serializer = HotelAccountSeriallizer(hotels, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"msg": "Error While Serializing"}, status=status.HTTP_400_BAD_REQUEST
            )


@permission_classes([IsAdminUser, IsAuthenticated])
class AdminPanelApprovedHotels(APIView):
    @swagger_auto_schema(
        tags=["Admin panel"],
        operation_description="Listing All Approved Hotels",
        responses={200: HotelAccountSeriallizer, 400: "errors"},
    )
    def get(self, request):
        hotels = HotelsAccount.objects.filter(Q(is_active=True) & Q(is_approved=True))
        try:
            count_hotels = len(hotels)
            pagination = CustomUserListPagination()
            count_pages = [
                i for i in range(1, (count_hotels // pagination.page_size) + 1)
            ]
            if count_hotels // pagination.page_size != 0:
                count_pages = [
                    i for i in range(1, (count_hotels // pagination.page_size) + 2)
                ]
            result_page = pagination.paginate_queryset(hotels, request)
            serializer = HotelAccountSeriallizer(result_page, many=True)
            return Response(
                {"data": serializer.data, "page_count": count_pages},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"msg": "Somthing Wrong while serialising"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class HotelSearch(APIView):
    def get(self, request):
        query = request.GET.get("q")
        if query:
            hotels = HotelsAccount.objects.filter(
                Q(hotel_name__icontains=query) | Q(email__icontains=query)
            )
            serializer = HotelAccountSeriallizer(hotels, many=True)
        else:
            return Response(
                {"msg": "No hotels available"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAdminUser, IsAuthenticated])
class AdminPanelUsersList(APIView):
    @swagger_auto_schema(
        tags=["Admin panel"],
        operation_description="Listing All Users",
        responses={200: UserSerilaizer, 400: "errors"},
    )
    def get(self, request):
        users = MyUser.objects.all()
        try:
            count_users = len(users)
            pagination = CustomUserListPagination()
            count_pages = count_users // pagination.page_size
            result_page = pagination.paginate_queryset(users, request)
            serializer = UserSerilaizer(result_page, many=True)
            return Response(
                {"data": serializer.data, "page_count": count_pages},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"msg": "Errors While Serializing"}, status=status.HTTP_400_BAD_REQUEST
            )


@permission_classes([IsAdminUser, IsAuthenticated])
class AdminPanelDeliveryPersonManage(APIView):
    def get(self, request):
        del_person = DeliveryPerson.objects.filter(is_approved=False)
        serializer = DeliveryPersonSerializer(del_person, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        id = request.GET.get("del_id")
        del_person = DeliveryPerson.objects.get(id=id)
        del_person.is_approved = True
        del_person.save()
        return Response(
            {"msg": "Approved the delivery person"}, status=status.HTTP_200_OK
        )


@permission_classes([IsAdminUser, IsAuthenticated])
class AdminPanelDeliveryPersonGet(APIView):
    def get(self, request):
        id = request.GET.get("del_id")
        if id:
            del_person = DeliveryPerson.objects.get(id=id)
            serializer = DeliveryPersonSerializer(del_person)
        else:
            del_person = DeliveryPerson.objects.filter(is_approved=True)
            serializer = DeliveryPersonSerializer(del_person, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Create your views here.
