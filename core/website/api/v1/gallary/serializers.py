from rest_framework import serializers
from website.models.gallary import Gallary
from website.models.users import User

class GallrySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Gallary
        fields = [
            "id",
            "owner",
            "title",
            "image",
            "like_count",
            "dislike_count",
            "description",
        ]
        
    def get_owner(self, obj):
        return self.context['request'].user.pk