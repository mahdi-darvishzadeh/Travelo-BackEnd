from rest_framework import viewsets
from rest_framework.response import Response
from website.models import Trip
from .serializers import *
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
    
class VoteAPIView(GenericAPIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'vote': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='The vote given by the clint',
                ),
            },
            required=['vote'],
        )
    )
    def post(self, request, pk):
        vote = request.data.get('vote')
        trip = Trip.objects.get(id=pk)
        if vote== 'like':
            trip.like_count += 1
            trip.save()
            trip_id = trip.pk
            return Response({'trip_id': trip_id, 'like_count': trip.like_count, 'dislike_count': trip.dislike_count})
        elif vote == 'dislike':
            trip.dislike_count += 1
            trip.save()
            trip_id = trip.pk
            return Response({'trip_id': trip_id, 'like_count': trip.like_count, 'dislike_count': trip.dislike_count})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)