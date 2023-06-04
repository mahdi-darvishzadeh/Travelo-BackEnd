from rest_framework import serializers
from website.models.profile import UserDetail

class ProfileSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    is_verified = serializers.BooleanField(source="user.is_verified" , read_only=True)
    rate = serializers.FloatField(source="user.rate" , read_only=True)
    trips_count = serializers.FloatField(source="user.trips_count" , read_only=True)

    class Meta:
        model = UserDetail
        fields = [
            "pk",
            "phone",
            "email",
            "first_name",
            "last_name",
            "rate",
            "trips_count",
            "image",
            "education",
            "job",
            "city",
            "description",
            "instagram",
            "gender",
            "marital_status",
            "is_verified",
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

        # total fields number is 18, which 3 of them are filled by django
        # [created_at, updated_at, id] so we subtract total from 3
        # 15 - 3 = 12, average formula will be: total / 12 * 100
        total = counter - 3
        percentage = round((total / 12) * 100)

        # add percentage to other representation fields
        data = super().to_representation(instance)
        data["completion_percentage"] = percentage
        data["age"] = instance.age
        return data