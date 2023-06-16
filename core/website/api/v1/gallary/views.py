from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from website.models.gallary import Gallary
from .serializers import GallryListSerializer
class AddToFavoriteView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        query_set = Gallary.objects.filter(admin_verify=True)
        q_top = query_set.order_by('-like_count')[:20]
        q_recent = query_set.order_by('-created_at')[:20]
        top_serializer = GallryListSerializer(q_top, many=True)
        recent_serializer = GallryListSerializer(q_recent, many=True)
        data = {
            'top': top_serializer.data,
            'recent': recent_serializer.data
        }
        return Response(data)
    