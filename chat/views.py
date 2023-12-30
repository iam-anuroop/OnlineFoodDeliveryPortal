# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageGetSerializer,MessagePostSerializer
from accounts.models import MyUser
from user_panel.models import ShoppingPayment


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message_data = request.data.get("message", {})
        text = message_data.get("text", "")
        sender = message_data.get("sender", "")
        chat_id = message_data.get("chat_id","")

        order_id = ShoppingPayment.objects.get(stripe_id=chat_id)

        serializer = MessagePostSerializer(data={"content": text})

        if serializer.is_valid():
            content = serializer.validated_data.get("content")
            sender = MyUser.objects.get(email=sender)
            # user = request.user
            # if sender != user:
            Message.objects.create(content=content, sender=sender, order_id=order_id)
            return Response({"msg": "message saved"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def get(self, request):
        try:
            chat_id = request.GET.get('chat_id')

            order_id = ShoppingPayment.objects.get(stripe_id=chat_id)

            messages = Message.objects.filter(order_id=order_id)
            serializer = MessageGetSerializer(messages, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except :
            return Response({'msg':'error occured'},status=status.HTTP_200_OK)




    


