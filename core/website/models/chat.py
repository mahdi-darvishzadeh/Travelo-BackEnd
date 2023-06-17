from django.db import models
from website.models import User, Trip

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True , blank = True, related_name='user')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null = True , blank = True, related_name='trip')
    unread_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.trip.owner.username} - {self.user.username}'
    
    def __json__(self):
        chat_as_dict = {}
        for k,v in self.__dict__.items():
            chat_as_dict[k] = v
        chat_as_dict["user"] = self.__dict__.get("user_id")
        chat_as_dict["trip"] = self.__dict__.get("trip_id")
        del chat_as_dict["_state"]

        return chat_as_dict

    class Meta:
        ordering = ['-created_at', '-updated_at']
