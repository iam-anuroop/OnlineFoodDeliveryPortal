# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InboxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        received_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)

        received_serializer = MessageSerializer(received_messages, many=True)
        sent_serializer = MessageSerializer(sent_messages, many=True)

        inbox_data = {
            'received_messages': received_serializer.data,
            'sent_messages': sent_serializer.data
        }

        return Response(inbox_data, status=status.HTTP_200_OK)
