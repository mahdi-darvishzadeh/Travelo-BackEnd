from re import search
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, status
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from website.models.users import User
from website.models.profile import UserDetail
from website.api.tools.api import CustomException
import phonenumbers

class SignupSerializer(serializers.Serializer):
    phone_or_email = serializers.CharField(max_length=255, required=True)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
    password2 = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        # check if password2 is the same as password
        if attrs["password2"] != attrs["password"]:
            raise CustomException(
                "رمزعبور ها یکسان نیستند!",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # validate password
        try:
            validate_password(attrs["password"])
        except:
            raise CustomException(
                "رمزعبور وارد شده صحیح نمیباشد.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # password2 is no longer needed
        attrs.pop("password2")

        # check if the given phone or email is unique
        result = detect_mobile_or_email_field(attrs["phone_or_email"])
        if result == "P":
            """phone is given"""
            q = User.objects.filter(phone=attrs["phone_or_email"])
            if q.exists():
                raise CustomException(
                    "کاربری با این شماره تلفن وجود دارد.",
                    "error",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        elif result == "E":
            """email is given"""
            q = User.objects.filter(email=attrs["phone_or_email"])
            if q.exists():
                raise CustomException(
                    "کاربری با این ایمیل وجود دارد.",
                    "error",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        elif result == "Error":
            """not phone or email is detected"""
            raise CustomException(
                "شماره تلفن یا ایمیل وارد شده صحیح نمیباشد.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # we need to send result of detect mobile or email function
        # to create method
        attrs["result"] = result
        return super().validate(attrs)

    def create(self, validated_data):
        result = validated_data["result"]
        if result == "P":
            user = User.objects.create_user(
                phone=validated_data["phone_or_email"],
                password=validated_data["password"],
            )
        elif result == "E":
            user = User.objects.create_user(
                email=validated_data["phone_or_email"],
                password=validated_data["password"],
            )

        # get the profile of user and attach firstname & lastname to it
        user_profile = UserDetail.objects.get(user=user)
        user_profile.first_name = validated_data["first_name"]
        user_profile.last_name = validated_data["last_name"]
        user_profile.save()

        # get access and refresh
        data = generate_JWT_access_refresh_token(user)
        return data


class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        # changing the default username field to phone_or_email
        self.username_field = "phone_or_email"
        return super().__init__(*args, **kwargs)

    def validate(self, attrs):
        # username can be phone or email
        # check is the phone_or_email is valid
        phone_or_email = attrs["phone_or_email"]
        result = detect_mobile_or_email_field(phone_or_email)

        if result == "Error":
            raise CustomException(
                "شماره تلفن یا ایمیل وارد شده صحیح نمیباشد.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # find user with the given phone or email
        try:
            user = User.objects.get(Q(phone=phone_or_email) | Q(email=phone_or_email))
        except User.DoesNotExist:
            raise CustomException(
                "کاربری با این اطلاعات وجود ندارد.",
                "error",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except:
            raise CustomException(
                "مشکلی در احراز هویت کاربر بوجود آمده است.",
                "error",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # authenticating user
        # authenticate function will return None
        # if user.is_active equals to false
        user = authenticate(username=user.username, password=attrs["password"])

        # is user password be incorrect, raise an exception
        try:
            refresh = self.get_token(user)
        except:
            raise CustomException(
                "رمزعبور به درستی وارد نشده است.",
                "error",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        update_last_login(None, user)

        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return data


"""Functions"""


def generate_JWT_access_refresh_token(user):
    """
    this function will generate a JWT access refresh token
    for the given user
    """
    refresh = RefreshToken.for_user(user)
    data = {"refresh": str(refresh), "access": str(refresh.access_token)}
    return data


def detect_mobile_or_email_field(value):
    """
    we have the same field for mobile and email
    and its upto our client to choose one,
    this function will detect that it is mobile or email
    """
    if search(r"^(\+98|0)?9\d{9}$" , value):
        phone = phonenumbers.parse(value , "IR")
        if phonenumbers.is_valid_number(phone):
            return "P"
        else :
            return "Error"
    elif search(r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$", value):
        return "E"
    else:
        return "Error"

