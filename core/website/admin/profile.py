from django.contrib import admin
from website.models import UserDetail


class UserDetailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "first_name",
        "last_name",
        "career",
        "gender",
        "birthdate",
        "trips_count",
        "rate",
        "created_at",
        "updated_at",
    ]
    list_filter = ["career", "gender", "education"]
    search_fields = [
        "first_name",
        "last_name",
        "education",
        "career",
        "user",
        "telegram",
        "instagram",
    ]
    ordering = ["id", "created_at", "updated_at"]


admin.site.register(UserDetail, UserDetailAdmin)
