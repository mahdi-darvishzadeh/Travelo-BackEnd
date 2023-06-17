from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializerCreate, ChatSerializerCreate, MessengerSerializerList, MessengerSerializerRetrieve
from website.models.chat import Chat
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

@parser_classes((MultiPartParser, FormParser))
class MessageCreateAPIView(GenericAPIView):    
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializerCreate
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ChatCreateAPIView(GenericAPIView):   
    permission_classes = [IsAuthenticated] 
    serializer_class = ChatSerializerCreate
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessangerViewSet(viewsets.ViewSet):
    def list(self, request):
        chats = Chat.objects.filter(Q(Q(user=request.user) | Q(trip__owner=request.user)))
        serializer = MessengerSerializerList(chats, many=True) 
        return Response(serializer.data)
    
    def retrieve(self, request,pk=None):
        chat = get_object_or_404(Chat, id=pk)
        serializer = MessengerSerializerRetrieve(chat)
        return Response(data=serializer.data)
