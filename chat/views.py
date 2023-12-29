# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from accounts.models import MyUser


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message_data = request.data.get("message", {})
        text = message_data.get("text", "")
        sender = message_data.get("sender", "")

        print("Text:", text)
        print("Sender:", sender)

        serializer = MessageSerializer(data={"content": text})

        if serializer.is_valid():
            content = serializer.validated_data.get("content")
            sender = MyUser.objects.get(email=sender)
            user = request.user
            if sender != user:
                Message.objects.create(content=content, sender=sender, receiver=user)
            return Response({"msg": "message saved"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InboxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        received_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)

        received_serializer = MessageSerializer(received_messages, many=True)
        sent_serializer = MessageSerializer(sent_messages, many=True)

        inbox_data = {
            "received_messages": received_serializer.data,
            "sent_messages": sent_serializer.data,
        }

        return Response(inbox_data, status=status.HTTP_200_OK)
