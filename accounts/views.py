from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import MyuserPhoneSerializer,MyuserEmailSerializer,OtpSerializer,TokenSerializer,GoogleAuthSerializer
from .utils import send_phone,verify_user_code,send_email
from rest_framework.response import Response
from rest_framework import status
from .models import MyUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
import random
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import base64
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def get_tokens_for_user(user,**kwargs):
    refresh = RefreshToken.for_user(user)
    
    access_token = TokenSerializer.get_token(user,**kwargs)

    return {
        'refresh': str(refresh),
        'access': str(access_token.access_token),
    }



class GoogleAuth(GenericAPIView):
    serializer_class = GoogleAuthSerializer

    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="Register of user using Google Authentication",
        responses={
            200:GoogleAuthSerializer,
            400:"errors"
        }
    )

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True )
        data = ((serializer.validated_data)['auth_token'])
        return Response(data,status=status.HTTP_200_OK)



class RegisterWithEmail(APIView):

    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="Register of user using email",
        responses={
            200:MyuserEmailSerializer,
            400:"errors"
        }
    )

    def post(self,request):
        serializer = MyuserEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp=random.randint(100000,999999)
            subject = "OTP for login."
            message = f"മോനെ ഇതാണ് നിന്റെ otp = {otp}"
            send_email(email=email,message=message,subject=subject)
            otp = str(otp)
            encoded_key = base64.b64encode(otp.encode('utf-8')).decode('utf-8')
            return Response({'msg':'OTP send to your mail...','otp':otp,'key':encoded_key,'email':email},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginWithOtp(APIView):

    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="Login using the OTP",
        responses={
            200:OtpSerializer,
            400:"errors"
        }
    )

    def post(self,request):
        serializer = OtpSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            key = request.data.get('key')
            login_email = request.data.get('email')
            login_otp = base64.b64decode(key.encode('utf-8')).decode('utf-8')
            if int(otp) == int(login_otp):
                try:
                    user = MyUser.objects.get(email=login_email)
                    token = get_tokens_for_user(user)
                    return Response({'token':token},status=status.HTTP_200_OK)
                except:
                    user = MyUser.objects.create_user(email=login_email)
                    user.is_active = True
                    user.save()
                    token = get_tokens_for_user(user)
                    return Response({'token':token},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'Invalid otp...'},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@permission_classes([IsAuthenticated])
class VerifyMobileNumber(APIView):

    @swagger_auto_schema(
        tags=["Phone Number Verification"],
        operation_description="Sending OTP through twilio",
        responses={
            200:OtpSerializer,
            400:"errors"
        }
    )
    def post(self,request):
        print(request.data)
        serilaizer = MyuserPhoneSerializer(data=request.data)
        if serilaizer.is_valid():
            phone = serilaizer.validated_data.get('phone')
            try:
                hashed_otp=send_phone(phone)
                return Response({'v_id':hashed_otp,'msg':'Otp sent successfully...'},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg':'Cant sent otp, Please try after sometimes...'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)



@permission_classes([IsAuthenticated])
class VerifyPhoneOtp(APIView):

    @swagger_auto_schema(
        tags=["Phone Number Verification"],
        operation_description="Verifying Twilio OTP",
        responses={
            200:OtpSerializer,
            400:"errors"
        }
    )
    
    def post(self,request):
        otp = request.data.get('otp')
        hashed_otp = request.data.get('v_id')
        phone = request.data.get('phone')
        print(otp,hashed_otp,phone)
        try:
            print('hiiii')
            verify_status = verify_user_code(hashed_otp,otp)
            user = request.user
            user = MyUser.objects.get(id=user.id)
            print('hooo')
            if verify_status == 'approved':
                user.phone = phone
                user.save()
                return Response({'msg':'Success...'},status=status.HTTP_200_OK)
            elif verify_status == 'rejected':
                return Response({'msg':'Wrong otp...'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'msg':'Somrthing wrong...'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'something wrong'},status=status.HTTP_400_BAD_REQUEST)



        





# Create your views here.

