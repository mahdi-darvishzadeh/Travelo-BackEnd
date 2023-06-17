from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import ProfileSerializer, TripSerializerList, ProfilePeopleSerializer, NotificationSerializerList
from website.models.profile import UserDetail
from website.models.users import User
from website.models.notification import Notification
from website.api.tools.api import CustomException
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from website.models.trip import Trip
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

@parser_classes((MultiPartParser, FormParser))
class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    def get_queryset(self, username):
        # return the user with the given username
        try:
            if username is None:
                user = User.objects.get(username=self.request.user.username)
                profile = UserDetail.objects.get(user=user)
                return profile
            else:
                user = User.objects.get(username=username)
                profile = UserDetail.objects.get(user=user)
                return profile
        except:
            raise CustomException(
                "کاربری با این شناسه وجود ندارد.",
                "error",
                status_code=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer Token',
                required=False,
            ),
        ]
    )
    def get(self, request, username=None, *args, **kwargs):
        query = self.get_queryset(username)
        serializer = self.serializer_class(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        if request.resolver_match.url_name != "profile-authorized": 
            return self.http_method_not_allowed(request, *args, **kwargs)
        query = self.get_queryset(username=request.user.username)
        serializer = self.serializer_class(query, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FavoriteTripViewSet(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    def list(self, request):
        userdetail = UserDetail.objects.get(user=request.user)
        data = []
        for favorite in userdetail.favorite:
            queryset = get_object_or_404(Trip, appear_in_search=True,pk=favorite)
            serializer = TripSerializerList(queryset, many=True)
            data.extend(serializer.data)
        return Response(data)
    
class MyTripViewSet(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    def list(self, request):
        queryset = Trip.objects.filter(owner=request.user)
        serializer = TripSerializerList(queryset, many=True)
        return Response(serializer.data)
    
class PeopleViewSet(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    def list(self, request):
        queryset = UserDetail.objects.all()
        q_most_eligible = queryset.order_by("-rate", "-trips_count")[:10]
        q_trip_Nearby = queryset.order_by("-created_at", "-trips_count")[:10]
        q_views = queryset.order_by("-rate", "-created_at")[:10]
        most_eligible_serializer = ProfilePeopleSerializer(q_most_eligible, many=True)
        trip_Nearby_serializer = ProfilePeopleSerializer(q_trip_Nearby, many=True)
        views_serializer = ProfilePeopleSerializer(q_views, many=True)
        data = {
            "most_eligible": most_eligible_serializer.data,
            "trip_Nearby": trip_Nearby_serializer.data,
            "views": views_serializer.data,
        }
        return Response(data)

class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        notification = Notification.objects.filter(owner=request.user)
        serializer =  NotificationSerializerList(notification, many=True)
        return Response(serializer.data)
    
class CheckStatusReadAPIView(GenericAPIView):  
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="The status read given by the user",
                ),
            },
            required=["status"],
        )
    )  
    def post(self, request, pk):
        status = request.data.get("status")
        notification = get_object_or_404(Notification, pk=pk, owner=request.user)
        notification.staus_read = status
        notification.save
        notification_pk = notification.pk
        notification.delete()
        return Response({"success": True , "pk" : notification_pk})    
    