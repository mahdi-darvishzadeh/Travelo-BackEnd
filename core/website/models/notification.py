from django.db import models
from website.models.users import User
from website.models.enums import NotificationEnum

class Notification(models.Model):
    owner = models.ForeignKey(User , on_delete = models.CASCADE , null = True , blank = True)
    staus_read = models.BooleanField(null=True, blank=True, default=False)
    title = models.CharField(
        max_length=255, choices=NotificationEnum.choices, default=NotificationEnum.CONFIRM_YOUR_EMAIL
    )

    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.owner.username
    
    def __json__(self):
        return {
            "id": self.pk,
            "owner": self.owner.username,
            "title": self.title,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }