from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from website.models import Trip
from .serializers import TripSearchSerializer
from datetime import datetime

class TripSearchGenericAPIView(GenericAPIView):
    serializer_class = TripSearchSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "from_city",
                openapi.IN_QUERY,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
            ),
            openapi.Parameter(
                "to_city",
                openapi.IN_QUERY,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
            ),
            openapi.Parameter(
                "moving_date",
                openapi.IN_QUERY,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING, format="date"),
            ),
            openapi.Parameter(
                "price",
                openapi.IN_QUERY,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        from_city_query = self.request.query_params.get("from_city", None)
        to_city_query = self.request.query_params.get("to_city", None)
        moving_day_query = self.request.query_params.get("moving_date", None)
        price_query = self.request.query_params.get("price", None)
        
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        queryset = Trip.objects.all()
        
        if from_city_query:
            queryset = queryset.filter(from_city=from_city_query)
        if to_city_query:
            queryset = queryset.filter(to_city=to_city_query)
        if moving_day_query:
            my_date = datetime.strptime(moving_day_query, "%Y-%m-%d").date()
            queryset = queryset.filter(
                moving_day__year=my_date.year,
                moving_day__month=my_date.month,
                moving_day__day=my_date.day,
            )
        if price_query:
            queryset = queryset.filter(price__lte=int(price_query))

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        