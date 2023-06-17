from rest_framework import serializers
from website.models.profile import UserDetail
from website.models.trip import Trip
from website.models.notification import Notification
from django.conf import settings

from django.urls import reverse

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, )
    is_verified = serializers.BooleanField(source="user.is_verified" , read_only=True)
    rate = serializers.FloatField(source="user.rate" , read_only=True)
    trips_count = serializers.FloatField(source="user.trips_count" , read_only=True)
    image = serializers.ImageField(required=False, )
    birthdate = serializers.DateField(required=False, input_formats=["%Y-%m-%d"])

    class Meta:
        model = UserDetail
        fields = [
            "pk",
            "phone",
            "email",
            "first_name",
            "last_name",
            "birthdate",
            "rate",
            "trips_count",
            "image",
            "education",
            "career",
            "living_in",
            "description",
            "telegram",
            "instagram",
            "gender",
            "marital_status",
            "phone_number",
            "personality_type",
            "workout",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["is_verified"]

    # def get_email(self, obj):
    #     return str(obj.user.email)

    def to_representation(self, instance):
        # calculate the profile completion percentage
        counter = 0
        for field in instance._meta.get_fields():
            field_value = getattr(instance, field.name)
            if field_value != None:
                counter += 1

        # total fields number is 23, which 6 of them are filled by django
        # [created_at, updated_at, id, favorite, trips_count, rate] so we subtract total from 6
        # 23 - 6 = 16, average formula will be: total / 16 * 100
        total = counter - 6
        percentage = round((total / 16) * 100)

        # add percentage to other representation fields
        data = super().to_representation(instance)
        data["completion_percentage"] = percentage
        data["age"] = instance.age
        data["image"] = str(instance.image) if instance.image else None
        return data
    
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
            "appear_in_search",
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
        return str(userdetail.image) if userdetail.image else None
        
class ProfilePeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetail
        fields = [
            "pk",
            "first_name",
            "last_name",
            "rate",
            "trips_count",
            "image",
            "education",
            "career",
            "living_in",
            "description",
            "telegram",
            "instagram",
            "gender",
            "marital_status",
            "personality_type",
            "workout",
            "created_at",
        ]

    def get_phone(self, obj):
        return str(obj.user.phone)

    def get_email(self, obj):
        return str(obj.user.email)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["age"] = instance.age
        data["image"] = str(instance.image) if instance.image else None
        return data
    
class NotificationSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
                  'pk',
                  'owner',
                  'title',
                  'created_at',
                  ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['owner'] = instance.owner.username
        return data