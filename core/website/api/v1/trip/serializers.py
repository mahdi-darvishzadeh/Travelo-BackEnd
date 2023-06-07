from rest_framework import serializers
from website.api.tools.api import CustomException
from django.urls import reverse
from rest_framework import status
from website.models import Trip, User

class TripSerializerCreate(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="pk",
        queryset=User.objects.all(),
        required=True,
    )

    class Meta:
        model = Trip
        fields = [
            "pk",
            "owner",
            "country",
            "from_city",
            "to_city",
            "moving_day",
            "Transportstion",
            "price",
            "description"
            ]

    def validate(self, attrs):
        return super().validate(attrs)
    