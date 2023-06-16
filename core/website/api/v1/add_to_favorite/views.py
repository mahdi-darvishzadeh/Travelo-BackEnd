from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from website.models.profile import UserDetail
from website.models.trip import Trip
from django.shortcuts import get_object_or_404

class AddToFavoriteView(GenericAPIView):
    def get(self, request, pk=None, *args, **kwargs):
        userdetail = get_object_or_404(UserDetail, user=request.user)
        if Trip.objects.filter(pk=pk).exists():
            if pk in userdetail.favorite:
                userdetail.favorite.remove(pk)
                userdetail.save()
                return Response(data={"message": "The desired trip has been successfully deleted from favorites"}, status=status.HTTP_200_OK)
            else:
                userdetail.favorite.append(pk)
                userdetail.save()
                return Response(data={"message": "The desired trip has been successfully saved in favorite"}, status=status.HTTP_200_OK)   
        else:
            return Response(data={"messege": "The desired trip was not found"}, status=status.HTTP_404_NOT_FOUND)
    