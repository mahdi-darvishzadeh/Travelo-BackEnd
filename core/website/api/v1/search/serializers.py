from rest_framework import serializers
from django.urls import reverse
from rest_framework import status
from website.models import Trip, UserDetail


class TripSearchSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    trip_owner_image = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        # appear_in_search is here for test
        exclude = [
            "owner",
            "updated_at",
        ]
    
    def get_fullname(self, obj):
        userdetail = UserDetail.objects.get(user=obj.owner)
        return f"{userdetail.first_name if userdetail.first_name else ''} {userdetail.last_name if userdetail.last_name else ''}"

    def get_absolute_url(self, obj):
        return reverse(
            "website:main-page:retrieve-trip", kwargs={"pk": obj.pk}
        )
    
    def get_trip_owner_image(self, obj):
        userdetail = UserDetail.objects.filter(user=obj.owner).first()
        return str(userdetail.image) if userdetail.image else None    
    