from django.shortcuts import render
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializer import (
    OwnerSerializer,
    HotelAccountSeriallizer,
    EmailSeriaizer,FoodmenuSerializer
) 
from accounts.views import get_tokens_for_user
from accounts.utils import send_email,send_phone,verify_user_code
from .models import HotelOwner,HotelsAccount,FoodMenu
from rest_framework.response import Response
from rest_framework import status
from accounts.models import MyUser
from accounts.serializers import OtpSerializer
import random
from .customauth import AuthenticateHotel
import base64
from django.db.models import Q



# Registration and updating of hotel owner details  

@permission_classes([IsAuthenticated])
class OwnerAccountView(APIView):
    def post(self,request):
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            owner = HotelOwner.objects.create(
                first_name = serializer.validated_data.get('first_name'),
                last_name = serializer.validated_data.get('last_name'),
                email = serializer.validated_data.get('email'),
                contact = serializer.validated_data.get('contact'),
                id_proof = serializer.validated_data.get('id_proof'),
                id_number = serializer.validated_data.get('id_number')
            )
            owner.user = user
            user.is_owner = True
            user.save()
            owner.save()
            subject = "You have a message"
            message = "Created the owner account continue and register your hotel"
            email = serializer.validated_data.get('email')
            send_email(email=email,subject=subject,message=message)
            return Response({'msg':'Account created...'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    # def patch(self,request):
    #     serializer = OwnerSerializer(HotelOwner,data=request.data,partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




# Registration and update profile for hotel account and sending otp for verifying phone number

@permission_classes([IsAuthenticated])
class HotelAccountRegister(APIView):
    def post(self,request):
        serializer = HotelAccountSeriallizer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            try:
                owner = HotelOwner.objects.get(user=request.user)
                email = serializer.validated_data.get('email')
                phone = serializer.validated_data.get('contact')
                hotel = HotelsAccount.objects.create(
                    hotel_name = serializer.validated_data.get('hotel_name'),
                    description = serializer.validated_data.get('description'),
                    certificate = serializer.validated_data.get('certificate'),
                    contact = phone,
                    alt_contact = serializer.validated_data.get('alt_contact'),
                    address = serializer.validated_data.get('address'),
                    email = email,
                    location = serializer.validated_data.get('location')
                )
                message = "Your requst for Adding Your hotel in our website is sussessfull, We will inform you ASAP"
                subject = "Hungry hub notification"
                send_email(message=message,subject=subject,email=email)
                hashed_otp = send_phone(phone)
                hotel.owner = owner
                hotel.save()
                return Response({'msg':'Registration request successfull...',
                                 'vid':hashed_otp,'phone':phone},status=status.HTTP_200_OK)
            except:
                return Response({'msg':'You are not a registered owner.'},status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def get(self,request):
        try:
            owner = HotelOwner.objects.get(user=request.user)
            hotels = HotelsAccount.objects.filter(owner=owner,is_active=True)
            serializer = HotelAccountSeriallizer(hotels,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'msg':'You are not a registered owner...'})
            


# verifying mobile through twilio while upadating and regitering the hotel account 

@permission_classes([IsAuthenticated])
class VerifyHotelPhone(APIView):
    def post(self,request):
        serializer = OtpSerializer(data=request.data)
        hashed_otp = request.data.get('vid')
        phone = request.data.get('phone')
        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            try:
                verify_status = verify_user_code(hashed_otp,otp)
                if verify_status == 'approved':
                    owner = HotelOwner.objects.get(user=request.user)
                    hotel = HotelsAccount.objects.get(owner=owner)
                    hotel.is_active = True
                    hotel.save()
                    return Response({'msg':'phone verification successfull...'},status=status.HTTP_200_OK)
                if verify_status == 'rejected':
                    return Response({'msg':'Invalid otp...'},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'msg':'Server error.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




# Hotel account login - sending otp to email

@permission_classes([IsAuthenticated])
class HotelLoginOtp(APIView):
    def post(self,request):
        try:
            owner = HotelOwner.objects.get(user=request.user)
            # serializer = EmailSeriaizer(data=request.data)
            # if serializer.is_valid():
                # hotel_email = serializer.validated_data.get('email')
                # print(hotel_email)
            hotel_id = request.data.get('hotel_id')
            hotel = HotelsAccount.objects.get(id=hotel_id,owner=owner)
            email = hotel.email
            subject = "Hungry hub code for Login"
            otp=random.randint(100000,999999)
            # request.session['otp']=otp
            # request.session['email']=email
            message = f"Your code for login is = {otp}"
            send_email(email=email,subject=subject,message=message)
            encoded_key = base64.b64encode(otp.encode('utf-8')).decode('utf-8')
            return Response({'msg':'Code has sent to registerd hotel mail your mail','otp':otp,'key':encoded_key,'email':email},status=status.HTTP_200_OK)
        except:
            return Response({'msg':'You are not a owner'},status=status.HTTP_400_BAD_REQUEST)


# hotel login with otp


@permission_classes([IsAuthenticated])
class HotelAccountLogin(APIView):
    def post(self,request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            # user_otp = serializer.validated_data.get('otp')
            # email = request.session.get('email')
            # otp = request.session.get('otp')
            otp = serializer.validated_data.get('otp')
            key = request.data.get('key')
            email = request.data.get('email')
            login_otp = base64.b64decode(key.encode('utf-8')).decode('utf-8')
            if int(login_otp) == int(otp):
                hotel = HotelsAccount.objects.get(email=email)
                # hotel.is_logined = True
                user = request.user
                token = get_tokens_for_user(user,hotel_email=hotel.email)
                return Response({'msg':'Login Successfull','token':token},status=status.HTTP_200_OK)
            return Response({'msg':'Invalid otp'},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    



@authentication_classes([AuthenticateHotel])
@permission_classes([IsAuthenticated])  
class HotelPhoneOtp(APIView):
    def post(self,request):
        hotel_email = request.auth
        if hotel_email:
            hotel = HotelsAccount.objects.get(email = hotel_email)
            hashed_otp = send_phone(hotel.contact)
            return Response({'msg':'Otp send to your registered numebr','vid':hashed_otp,'phone':hotel.contact},status=status.HTTP_200_OK)
        return Response({'msg':'login before tryyy...!'},status=status.HTTP_400_BAD_REQUEST)





@authentication_classes([AuthenticateHotel])
@permission_classes([IsAuthenticated])
class FoodmenuView(APIView):
    def post(self,request):
        hotel_email = request.auth
        if hotel_email:
            hotel = HotelsAccount.objects.get(email=hotel_email)
            serializer = FoodmenuSerializer(data=request.data)
            if serializer.is_valid():
                food = FoodMenu.objects.create(
                    food_name = serializer.validated_data.get('food_name'),
                    food_type = serializer.validated_data.get('food_type'),
                    food_image = serializer.validated_data.get('food_image'),
                    food_price = serializer.validated_data.get('food_price'),
                    description = serializer.validated_data.get('description'),
                    is_veg = serializer.validated_data.get('is_veg')
                )
                food.hotel = hotel
                food.save()
                return Response({'msg':'food item added'},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        return Response({'msg':'You are not logined'},status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request):
        hotel_email = request.auth
        if hotel_email:
            # hotel = HotelsAccount.objects.get(email = hotel_email)
            id = request.data.get('id')
            food = FoodMenu.objects.get(id=id)
            serializer = FoodmenuSerializer(food,data=request.data,partial=True)
            if serializer.is_valid():
                food.food_name = serializer.validated_data.get('food_name')
                food.food_type = serializer.validated_data.get('food_type')
                food.food_image = serializer.validated_data.get('food_image')
                food.food_price = serializer.validated_data.get('food_price')
                food.description = serializer.validated_data.get('description')
                food.is_veg = serializer.validated_data.get('is_veg')
                food.is_available = serializer.validated_data.get('is_available')

                food.save()
                return Response({'msg':'updated'},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'something wrooong'},status=status.HTTP_400_BAD_REQUEST)
    


    def get(self,request):
        hotel_email = request.auth
        hotel = HotelsAccount.objects.get(email=hotel_email)
        query = request.GET.get('q')
        if query:
            hotels = FoodMenu.objects.filter(
                Q(hotel=hotel) &
                Q(food_name__icontains=query) |
                Q(description__icontains=query) |
                Q(food_type__icontains=query)
                )
        else:
            hotels = FoodMenu.objects.filter(hotel=hotel)
        return render(request, 'hotel_search.html', {'hotels': hotels, 'query': query})
            







# Create your views here.













    # Theatre patch

    # def patch(self,request):
    #     try:
    #         owner = HotelOwner.objects.get(user=request.user)
    #         hotel = HotelsAccount.objects.get(owner=owner)
    #         serializer = HotelAccountSeriallizer(HotelsAccount,request.data,partial=True)
    #         if serializer.is_valid():
    #             email = serializer.validated_data.get('email')
    #             phone = serializer.validated_data.get('contact')
    #             message = "Updated Your Hotel profile."
    #             subject = "Hungry hub ."
    #             send_email(message=message,subject=subject,email=email)
    #             if hotel.contact != phone:
    #                 hotel.is_active = False
    #                 hashed_otp = send_phone(phone)
    #                 request.session['hashed_otp'] = hashed_otp
    #                 request.session['phone'] = phone
    #                 hotel.save()
    #             serializer.save()
    #             # please verify your phone alert while changing the phone number
    #             return Response(serializer.data,status=status.HTTP_200_OK)
    #         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    #     except:
    #         return Response({'Register owner form first...'},status=status.HTTP_400_BAD_REQUEST)