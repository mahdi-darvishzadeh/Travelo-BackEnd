from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import ProfileSerializer, TripSerializerList
from website.models.profile import UserDetail
from website.models.users import User
from website.api.tools.api import CustomException
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from website.models.trip import Trip
from rest_framework.permissions import IsAuthenticated

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
            queryset = Trip.objects.filter(appear_in_search=True,pk=favorite)
            serializer = TripSerializerList(queryset, many=True)
            data.extend(serializer.data)
        return Response(data)
    
class MyTripViewSet(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    def list(self, request):
        queryset = Trip.objects.filter(owner=request.user)
        serializer = TripSerializerList(queryset, many=True)
        return Response(serializer.data)
    