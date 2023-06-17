from django.contrib import admin
from django.db import models
from django.forms import BooleanField
from website.models.notification import Notification

class ToggleBooleanWidget(BooleanField.widget):
    template_name = "toggle_button.html"


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "title", "updated_at", "created_at"]
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("owner__username", "title")

admin.site.register(Notification, NotificationAdmin)