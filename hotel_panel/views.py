from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializer import OwnerSerializer,HotelAccountSeriallizer
from accounts.utils import send_email,send_phone,verify_user_code
from .models import HotelOwner,HotelsAccount
from rest_framework.response import Response
from rest_framework import status
from accounts.models import MyUser
from accounts.serializers import OtpSerializer
import random



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
            subject = "You have a message"
            message = "Created the owner account continue and register your hotel"
            email = serializer.validated_data.get('email')
            send_email(email=email,subject=subject,message=message)
            return Response({'msg':'Account created...'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request):
        serializer = OwnerSerializer(HotelOwner,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




# Registration and update profile for hotel account and sending otp for verifying phone number

@permission_classes([IsAuthenticated])
class HotelAccountRegister(APIView):
    def post(self,request):
        try:
            serializer = HotelAccountSeriallizer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email'),
                phone = serializer.validated_data.get('contact'),
                hotel = HotelsAccount.objects.create(
                    hotel_name = serializer.validated_data.get('hotel_name'),
                    description = serializer.validated_data.get('description'),
                    alt_contact = serializer.validated_data.get('alt_contact'),
                    certificate = serializer.validated_data.get('certificate'),
                    contact = phone,
                    email = email,
                    address = serializer.validated_data.get('adress'),
                    location = serializer.validated_data.get('location'),
                )
                message = "Your requst for Adding Your hotel in our website is sussessfull, We will inform you ASAP"
                subject = "Hungry hub notification"
                send_email(message=message,subject=subject,email=email)
                hashed_otp = send_phone(phone)
                request.session['hashed_otp'] = hashed_otp
                request.session['phone'] = phone
                owner = HotelOwner.objects.get(user=request.user)
                hotel.owner = owner
                hotel.save()
                return Response({'msg':'Registration request successfull...'},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'msg':'You are not a registered owner.'},status=status.HTTP_400_BAD_REQUEST)




    def patch(self,request):
        try:
            owner = HotelOwner.objects.get(user=request.user)
            hotel = HotelsAccount.objects.get(owner=owner)
            serializer = HotelAccountSeriallizer(HotelsAccount,request.data,partial=True)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                phone = serializer.validated_data.get('contact')
                message = "Updated Your Hotel profile."
                subject = "Hungry hub ."
                send_email(message=message,subject=subject,email=email)
                if hotel.contact != phone:
                    hotel.is_active = False
                    hashed_otp = send_phone(phone)
                    request.session['hashed_otp'] = hashed_otp
                    request.session['phone'] = phone
                    hotel.save()
                serializer.save()
                # please verify your phone alert while changing the phone number
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'Register owner form first...'},status=status.HTTP_400_BAD_REQUEST)
            


# verifying mobile through twilio while upadating and regitering the hotel account 

@permission_classes([IsAuthenticated])
class VerifyHotelPhone(APIView):
    def post(self,request):
        serializer = OtpSerializer(data=request.data)
        hashed_otp = request.session.get('hashed_otp')
        phone = request.session.get('phone')
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
            hotel = HotelsAccount.objects.get(owner=owner)
            email = hotel.email
            subject = "Hungry hub code for Login"
            otp=random.randint(100000,999999)
            request.session['otp']=otp
            request.session['email']=email
            message = f"Your code for login is = {otp}"
            send_email(email=email,subject=subject,message=message)
            return Response({'msg':'Code has sent to your mail'},status=status.HTTP_200_OK)
        except:
            return Response({'msg':'You are not a owner'},status=status.HTTP_400_BAD_REQUEST)



@permission_classes([IsAuthenticated])
class HotelAccountLogin(APIView):
    def post(self,request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            user_otp = serializer.validated_data.get('otp')
            email = request.session.get('email')
            otp = request.session.get('otp')
            if user_otp == otp:
                hotel = HotelsAccount.objects.get(email=email)
                hotel.is_logined = True
                return Response({'msg':'Login Successfull'},status=status.HTTP_200_OK)
            return Response({'msg':'Invalid otp'},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





# Create your views here.
