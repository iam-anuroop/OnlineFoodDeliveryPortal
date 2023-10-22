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



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    access_token = TokenSerializer.get_token(user)

    return {
        'refresh': str(refresh),
        'access': str(access_token.access_token),
    }



class GoogleAuth(GenericAPIView):
    serializer_class = GoogleAuthSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True )
        data = ((serializer.validated_data)['auth_token'])
        return Response(data,status=status.HTTP_200_OK)


class RegisterWithEmail(APIView):
    def post(self,request):
        serializer = MyuserEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp=random.randint(100000,999999)
            print(otp)
            subject = "OTP for login."
            send_email(email=email,otp=otp,subject=subject)
            request.session['login_otp'] = otp
            request.session['login_email'] = email
            return Response({'msg':'OTP send to your mail...'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginWithOtp(APIView):
    def post(self,request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            login_otp = request.session.get('login_otp')
            login_email = request.session.get('login_email')
            if otp == login_otp:
                try:
                    user = MyUser.objects.get(email=login_email)
                    token = get_tokens_for_user(user)
                    return Response({'token':token},status=status.HTTP_200_OK)
                except:
                    user = MyUser.objects.create_user(email=login_email)
                    token = get_tokens_for_user(user)
                    return Response({'token':token},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'Invalid otp...'},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class VerifyMobileNumber(APIView):
    def post(self,request):
        print(request.data)
        serilaizer = MyuserPhoneSerializer(data=request.data)
        if serilaizer.is_valid():
            phone = serilaizer.validated_data.get('phone')
            try:
                hashed_otp=send_phone(phone)
                request.session['hashed_otp']=hashed_otp
                request.session['phone']=phone
                return Response({'data':serilaizer.data,'msg':'Otp sent successfully...'},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg':'Cant sent otp, Please try after sometimes...'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneOtp(APIView):
    def post(self,request):
        serilaizer = OtpSerializer(data=request.data)
        if serilaizer.is_valid():
            otp = serilaizer.validated_data.get('otp')
            hashed_otp = request.session.get('hashed_otp')
            phone = request.session.get('phone')
            try:
                verify_status = verify_user_code(hashed_otp,otp)
                user = request.user
                user = MyUser.objects.get(id=10)
                if verify_status == 'approved':
                    user.phone = phone
                    user.save()
                    return Response({'msg':'Success...'},status=status.HTTP_200_OK)
                elif verify_status == 'rejected':
                    return Response({'msg':'Wrong otp...'},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'msg':'Somrthing wrong...'},status=status.HTTP_400_BAD_REQUEST)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)



        





# Create your views here.

