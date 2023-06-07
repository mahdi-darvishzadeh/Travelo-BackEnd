from django.db import models
from website.models import User

class Trip(models.Model):
    owner = models.ForeignKey(User , on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=255)
    from_city = models.CharField(null=True, blank=True, max_length=255)
    to_city = models.CharField(null=True, blank=True, max_length=255)
    moving_day = models.DateTimeField(null=True, blank=True)
    Transportstion = models.CharField(null=True, blank=True, max_length=255)
    price = models.IntegerField(default=0, max_length=20, null=True, blank=True)
    like_count = models.IntegerField(default=0, max_length=20, null=True, blank=True)
    dislike_count = models.IntegerField(default=0, max_length=20, null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    appear_and_search = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-moving_day']

    def __str__(self):
        return f'{self.owner.username}'
    