from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple, BooleanField, ClearableFileInput
from website.models.chat import Chat
from website.models.message import Message

class ToggleBooleanWidget(BooleanField.widget):
    template_name = "toggle_button.html"

class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "trip", "unread_count"]
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("user__username", "trip__owner__username")

class ToggleBooleanWidget(BooleanField.widget):
    template_name = "toggle_button.html"

class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "chat", "author", "created_at", "is_seen"]
    search_fields = ["chat__id", ]
    formfield_overrides = {
        models.ImageField: {"widget": ClearableFileInput},
    }

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)