from rest_framework import serializers
from website.models.profile import UserDetail
from website.models.trip import Trip
from django.urls import reverse

class ProfileSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
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

    def get_phone(self, obj):
        return str(obj.user.phone)

    def get_email(self, obj):
        return str(obj.user.email)

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
        return data
    
class TripSerializerList(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        # appear_in_search is here for test
        fields = [
            "pk",
            "absolute_url",
            "moving_day",
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