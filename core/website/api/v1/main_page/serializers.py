from rest_framework import serializers
from website.api.tools.api import CustomException
from django.urls import reverse
from rest_framework import status
from website.models import Trip, User


class TripSerializerList(serializers.ModelSerializer):
    # absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        # appear_in_search is here for test
        fields = [
            "pk",
            "moving_day",
            "from_city",
            "to_city",
            "Transportstion",
            "price",
            "like_count",
            "dislike_count",
            "appear_and_search",
            "created_at",
        ]

    # def get_absolute_url(self, obj):
    #     return reverse(
    #         "website:main-page:retrieve-trip", kwargs={"pk": obj.pk}
    #     )
    
