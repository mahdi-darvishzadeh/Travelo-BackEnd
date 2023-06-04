from django.contrib import admin
from django.db import models
from django.forms import BooleanField, ClearableFileInput
from website.models.trip import Trip

class ToggleBooleanWidget(BooleanField.widget):
    template_name = "toggle_button.html"


class TripAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "country", "from_city", "to_city", "moving_day", "like_count", "dislike_count", "rate", "price", "created_at"]
    formfield_overrides = {
        models.ImageField: {"widget": ClearableFileInput},
    }
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("owner", "from_city", "to_city", "moving_day", "country")

admin.site.register(Trip, TripAdmin)
