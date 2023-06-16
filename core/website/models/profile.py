from django.db import models
from website.models.users import User
from django.db.models.signals import post_save
from django.contrib.postgres import fields as pgmodels
from django.dispatch import receiver
from datetime import date
from rest_framework import status
from website.api.tools.api import CustomException

# Create profile object after user creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)

# from website.models.profile import UniqueArrayField
class UniqueArrayField(pgmodels.ArrayField):
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        
        if len(value) != len(set(value)):
            raise CustomException(
                "Values in the array must be unique.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST
                )

class UserDetail(models.Model):
    # available in Profile endpoint
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    career = models.CharField(max_length=255, null=True, blank=True)
    living_in = models.CharField(max_length=255, null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    trips_count = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="profile_image/")
    personality_type = models.CharField(max_length=255, null=True, blank=True)
    workout = models.CharField(max_length=255, null=True, blank=True)
    favorite = UniqueArrayField(models.CharField(max_length=255), null=True, blank=True)

    # extra information
    gender = models.CharField(max_length=255, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True)
    telegram = models.CharField(max_length=255, unique=True, null=True, blank=True)
    instagram = models.CharField(max_length=255, unique=True, null=True, blank=True)

    # system information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"UserDetail obj: {self.id}-{self.first_name,self.last_name}"

    @property
    def age(self):
        today = date.today()
        if self.birthdate != None:
            age = (
                today.year
                - self.birthdate.year
                - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
            )
            return age
        
