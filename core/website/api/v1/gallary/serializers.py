from rest_framework import serializers
from website.models.gallary import Gallary
from website.models.users import User

class GallrySerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="pk",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        required=False,
    )
    
    class Meta:
        model = Gallary
        fields = [
            "pk",
            "owner",
            "title",
            "image",
            "like_count",
            "dislike_count",
            "description",
        ]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = str(instance.image) if instance.image else None
        return data