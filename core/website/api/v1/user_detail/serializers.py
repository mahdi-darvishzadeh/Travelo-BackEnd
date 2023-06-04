from rest_framework import serializers
from website.models.profile import UserDetail
from django.urls import reverse

class ProfileSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    is_verified = serializers.BooleanField(source="user.is_verified" , read_only=True)

    class Meta:
        model = UserDetail
        fields = [
            "pk",
            "phone",
            "email",
            "fullname",
            "education",
            "job",
            "city",
            "favorite",
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

        # total fields number is 24, which 3 of them are filled by django
        # [created_at, updated_at, id] so we subtract total from 3
        # 24 - 3 = 21, average formula will be: total / 21 * 100
        total = counter - 3
        percentage = round((total / 22) * 100)

        # add percentage to other representation fields
        data = super().to_representation(instance)
        data["completion_percentage"] = percentage
        data["age"] = instance.age
        return data