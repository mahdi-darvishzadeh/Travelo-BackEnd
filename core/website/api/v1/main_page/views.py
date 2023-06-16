from rest_framework import viewsets
from rest_framework.response import Response
from website.models import Trip
from .serializers import TripSerializerList, TripSerializerRetrieve
from django.shortcuts import get_object_or_404

class TripViewSet(viewsets.ModelViewSet):
    def list(self, request):
        queryset = Trip.objects.filter(appear_in_search=True,)
        q_best_driver = queryset.order_by("-rate", "-like_count")[:20]
        q_trip_for_now = queryset.order_by("-created_at", "-moving_day")[:20]
        best_driver_serializer = TripSerializerList(
            q_best_driver, many=True
        )
        trip_for_now_serializer = TripSerializerList(q_trip_for_now, many=True)
        data = {
            "best_driver": best_driver_serializer.data,
            "trip_for_now": trip_for_now_serializer.data,
        }
        return Response(data)

    def retrieve(self, request, pk=None):
        trip = get_object_or_404(Trip, pk=pk, appear_in_search=True)
        serializer = TripSerializerRetrieve(trip)
        return Response(serializer.data)