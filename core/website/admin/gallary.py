from django.contrib import admin
from django.db import models
from django.forms import BooleanField, ClearableFileInput
from website.models.gallary import Gallary

class ToggleBooleanWidget(BooleanField.widget):
    template_name = "toggle_button.html"


class GallaryAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "like_count", "dislike_count", "created_at"]
    formfield_overrides = {
        models.ImageField: {"widget": ClearableFileInput},
    }
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("owner", )

admin.site.register(Gallary, GallaryAdmin)
