from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import MyuserEmailSerializer,OtpSerializer,TokenSerializer,GoogleAuthSerializer
from .utils import send_email,verify_user_code
from rest_framework.response import Response
from rest_framework import status
from .models import MyUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView



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



class RegistrationClass(APIView):
    def post(self,request):
        serilaizer = MyuserEmailSerializer(data=request.data)
        if serilaizer.is_valid():
            email = serilaizer.validated_data.get('phone')
            print(email)
            try:
                hashed_otp=send_email(email)
                request.session['hashed_otp']=hashed_otp
                request.session['email']=email
                return Response({'data':serilaizer.data,'msg':'Otp sent successfully...'},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg':'Cant sent otp, Please try after sometimes...'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)



class OtpVerification(APIView):
    def post(self,request):
        serilaizer = OtpSerializer(data=request.data)
        if serilaizer.is_valid():
            otp = serilaizer.validated_data.get('otp')
            hashed_otp = request.session.get('hashed_otp')
            email = request.session.get('email')
            try:
                verify_status = verify_user_code(hashed_otp,otp)
                if verify_status == 'approved':
                    user = MyUser.objects.create_user(email=email)
                    user.is_active=True
                    user.save()
                    if user is not None:
                        token = get_tokens_for_user(user)
                        return Response({'msg':'Success...','token':token},status=status.HTTP_200_OK)
                elif verify_status == 'rejected':
                    return Response({'msg':'Wrong otp...'},status=status.HTTP_400_BAD_REQUEST)
                return Response({'msg':'Something went wrong...'},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({'msg':'Somrthing wrong...'},status=status.HTTP_400_BAD_REQUEST)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
                


# Create your views here.
