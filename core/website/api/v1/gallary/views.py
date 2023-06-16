from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from website.models.gallary import Gallary
from .serializers import GallrySerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


class GallaryView(GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        query_set = Gallary.objects.filter(admin_verify=True)
        q_top = query_set.order_by('-like_count')[:20]
        q_recent = query_set.order_by('-created_at')[:20]
        top_serializer = GallrySerializer(q_top, many=True)
        recent_serializer = GallrySerializer(q_recent, many=True)
        data = {
            'top': top_serializer.data,
            'recent': recent_serializer.data
        }
        return Response(data)
    
@parser_classes((MultiPartParser, FormParser))
class GallaryCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GallrySerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)