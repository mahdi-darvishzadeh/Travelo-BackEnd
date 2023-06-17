from django.db import models
from website.models.users import User
from website.models.chat import Chat
from django.conf import settings

class Message(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True, related_name='author')
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE, null = True, blank = True, related_name='chat')
    content = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to="message-file/")
    replay = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)
    is_seen = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.username
    
    def __json__(self):
        return {
            "message_id": self.id,
            "author": self.author.id,
            "content": self.content,
            "file" : settings.MEDIA_URL + str(self.file) if self.file else None,
            "replay" : None if not self.replay else self.replay.id,
            "is_seen" : self.is_seen,
            "created_at" : self.created_at,
        }
    
    class Meta:
        ordering = ['-created_at']

    @staticmethod
    def get_all():
        return [m.content for m in Message.objects.all()]