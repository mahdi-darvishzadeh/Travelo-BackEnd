from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import ProfileSerializer
from website.models.profile import UserDetail
from website.models.users import User
from website.api.tools.api import CustomException
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    