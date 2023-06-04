from django.db import models
from website.models.users import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from rest_framework import status

# Create profile object after user creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)


class UserDetail(models.Model):
    # available in Profile endpoint
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    job = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    # extra information
    gender = models.CharField(max_length=255, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=255, null=True, blank=True)
    favorite = models.TextField(null=True, blank=True)
    telegram = models.CharField(max_length=255, unique=True, null=True, blank=True)
    instagram = models.CharField(max_length=255, unique=True, null=True, blank=True)

    # system information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"UserDetail obj: {self.id}-{self.fullname}"

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
