from django.db import models
from website.models import User

class Gallary(models.Model):
    owner = models.ForeignKey(User , on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="gallary/")
    description = models.TextField(null=True, blank=True)
    like_count = models.IntegerField(default=0, max_length=20, null=True, blank=True)
    dislike_count = models.IntegerField(default=0, max_length=20, null=True, blank=True)
    
    admin_verify = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner.username}'
    