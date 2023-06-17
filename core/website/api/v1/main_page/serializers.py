from rest_framework import serializers
from website.api.tools.api import CustomException
from django.urls import reverse
from rest_framework import status
from website.models import Trip, User, UserDetail
from django.conf import settings


class TripSerializerList(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    trip_owner_fullname = serializers.SerializerMethodField()
    trip_owner_image = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        # appear_in_search is here for test
        fields = [
            "pk",
            "absolute_url",
            "trip_owner_fullname",
            "trip_owner_image",
            "moving_day",
            "day_to",
            "from_city",
            "to_city",
            "Transportstion",
            "price",
            "like_count",
            "dislike_count",
            "rate",
            "created_at",
        ]

    def get_absolute_url(self, obj):
        return reverse(
            "website:main-page:retrieve-trip", kwargs={"pk": obj.pk}
        )
    
    def get_trip_owner_fullname(self, obj):
        userdetail = UserDetail.objects.filter(user=obj.owner).first()
        return userdetail.fullname if userdetail else None
    
    def get_trip_owner_image(self, obj):
        userdetail = UserDetail.objects.filter(user=obj.owner).first()
        return settings.MEDIA_URL + str(userdetail.image) if userdetail.image else None
    
class TripSerializerRetrieve(serializers.ModelSerializer):

    class Meta:
        model = Trip
        exclude = [
            "updated_at"
        ]
    