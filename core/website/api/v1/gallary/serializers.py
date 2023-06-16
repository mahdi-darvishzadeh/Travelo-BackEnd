from rest_framework import serializers
from website.models.gallary import Gallary

class GallryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallary
        fields = [
            "id",
            "title",
            "image",
            "like_count",
            "dislike_count",
            "description",
        ]