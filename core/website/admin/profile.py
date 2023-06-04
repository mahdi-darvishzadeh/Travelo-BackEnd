from django.contrib import admin
from website.models import UserDetail


class UserDetailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "first_name",
        "last_name",
        "job",
        "gender",
        "birthdate",
        "trips_count",
        "rate",
        "created_at",
        "updated_at",
    ]
    list_filter = ["job", "gender", "education"]
    search_fields = [
        "fullname",
        "education",
        "job",
        "user",
        "telegram",
        "instagram",
    ]
    ordering = ["id", "created_at", "updated_at"]


admin.site.register(UserDetail, UserDetailAdmin)
