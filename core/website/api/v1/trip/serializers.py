from rest_framework import serializers
from website.api.tools.api import CustomException
from django.urls import reverse
from rest_framework import status
from website.models import Trip, User
from datetime import datetime

class TripSerializerCreate(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="pk",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        required=False,
    )
    moving_day = serializers.DateField(input_formats=["%Y-%m-%d"])
    day_to = serializers.DateField(input_formats=["%Y-%m-%d"])

    class Meta:
        model = Trip
        fields = [
            "pk",
            "owner",
            "country",
            "from_city",
            "to_city",
            "moving_day",
            "day_to",
            "Transportstion",
            "price",
            "description"
            ]

    def validate(self, attrs):
        moving_day = attrs.get("moving_day")
        if moving_day:
            return super().validate(attrs)
        else:
            raise serializers.ValidationError("Invalid date")
    