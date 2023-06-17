from django.urls import reverse
from rest_framework import serializers
from website.models.chat import Chat
from website.models.message import Message
from website.models.users import User
from website.models.profile import UserDetail
from website.models.trip import Trip
from django.db.models import F

class MessageSerializerCreate(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="pk",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        required=False,
    )
    chat = serializers.SlugRelatedField(
        slug_field="pk",
        queryset=Chat.objects.all(),
        required=True,
    )
    
    class Meta:
        model = Message
        fields  = [
            "pk",
            "author",
            "chat",
            "content",
            "file",
            "replay",
            "is_seen",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "is_seen"
        ]

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        replay = validated_data.pop('replay', None)
        message = Message.objects.create(**validated_data)
        if file:
            message.file = file
        if message.chat:
            message.chat.unread_count = F('unread_count') + 1
            message.chat.save()
        if replay:
            message.replay = replay
        message.save()
        return message
    
    def validate(self, attrs):
        chat = attrs.get("chat")
        author = attrs.get("author")
        if (chat.user or chat.trip.owner) == author:
            return super().validate(attrs)
        else:
            raise serializers.ValidationError("Invalid date")
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = instance.author.username
        return data
    
class ChatSerializerCreate(serializers.ModelSerializer): 
    trip = serializers.SlugRelatedField(
        slug_field="pk",
        queryset=Trip.objects.all(),
        required=True,
    )
    user = serializers.SlugRelatedField(
        slug_field="pk",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        required=False,
    )
    
    class Meta:
        model = Chat
        fields = [
            "pk",
            "user",
            "trip",
            "unread_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["unread_count"]

    def create(self, validated_data):
        chat, created = Chat.objects.get_or_create(**validated_data)
        return chat
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.username if instance.user else None
        data["trip"] = instance.trip.owner.username
        data["unread_count"] = instance.unread_count
        return data

class MessengerSerializerList(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    user_career = serializers.SerializerMethodField()
    user_fullname = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    trip_owner_career = serializers.SerializerMethodField()
    trip_owner_fullname = serializers.SerializerMethodField()
    trip_owner_image = serializers.SerializerMethodField()

    def get_absolute_url(self, obj:Chat):
        return reverse(
            "website:messenger:retrieve-contact", kwargs={"pk": obj.pk}
            )
    
    def get_user_career(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.user).first()
        return userdetail.career if userdetail else None
    
    def get_user_fullname(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.user).first()
        return userdetail.fullname if userdetail else None
    
    def get_user_image(self, obj):
        userdetail = UserDetail.objects.filter(user=obj.user).first()
        return str(userdetail.image) if userdetail.image else None
    
    def get_trip_owner_career(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.trip.owner).first()
        return userdetail.career if userdetail else None

    def get_trip_owner_fullname(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.trip.owner).first()
        return userdetail.fullname if userdetail else None
    
    def get_trip_owner_image(self, obj):
        userdetail = UserDetail.objects.filter(user=obj.trip.owner).first()
        return str(userdetail.image) if userdetail.image else None
    
    class Meta:
        model = Chat
        exclude = [
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user_id'] = instance.user.id
        data['trip_id'] = instance.trip.id
        data['user_username'] = instance.user.username
        data['trip_owner_username'] = instance.trip.owner.username
        data['unread_count'] = instance.unread_count
        return data

class MessengerSerializerRetrieve(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    user_career = serializers.SerializerMethodField()
    trip_owner_career = serializers.SerializerMethodField()
    user_fullname = serializers.SerializerMethodField()
    trip_owner_fullname = serializers.SerializerMethodField()
    user_living_in = serializers.SerializerMethodField()
    trip_owner_living_in = serializers.SerializerMethodField()
    trip_rate = serializers.SerializerMethodField()
    trip_owner_image = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()

    def get_messages(self,obj):
        return [message.__json__() for message in Message.objects.filter(chat=obj.id)]
    
    def get_user_career(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.user).first()
        return userdetail.career if userdetail else None
    
    def get_trip_owner_career(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.trip.owner).first()
        return userdetail.career if userdetail else None

    def get_user_fullname(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.user).first()
        return userdetail.fullname if userdetail else None
    
    def get_trip_owner_fullname(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.trip.owner).first()
        return userdetail.fullname if userdetail else None
    
    def get_user_living_in(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.user).first()
        return userdetail.living_in if userdetail else None
    
    def get_trip_owner_living_in(self, obj:Chat):
        userdetail = UserDetail.objects.filter(user=obj.trip.owner).first()
        return userdetail.living_in if userdetail else None
    
    def get_trip_rate(self, obj:Chat):
        trip = Trip.objects.filter(pk=obj.trip.pk).first()
        return trip.rate if trip else None
    
    def get_user_image(self, obj):
        userdetail = UserDetail.objects.filter(user=obj.user).first()
        return str(userdetail.image) if userdetail.image else None
    
    def get_trip_owner_image(self, obj):
        userdetail = UserDetail.objects.filter(user=obj.trip.owner).first()
        return str(userdetail.image) if userdetail.image else None
    
    class Meta:
        model = Chat
        exclude = [
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)   
        queryset_message = Message.objects.filter(chat=instance)
        for message in queryset_message:
            if message.is_seen == False :
                message.chat.unread_count = message.chat.unread_count - 1
                message.chat.save()
            message.is_seen = True
            message.save()
        return data
    