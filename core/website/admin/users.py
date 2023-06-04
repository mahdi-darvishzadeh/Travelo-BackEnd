from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from website.models import User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "id",
        "email",
        "phone",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "phone", "username")
    ordering = ("created_at", "updated_at", "id")
    fieldsets = (
        ("Authentication", {"fields": ("email", "phone", "username", "password")}),
        (
            "Permissions",
            {"fields": ("is_superuser", "is_staff", "is_active", "is_verified")},
        ),
    )
    add_fieldsets = (
        (
            "Registration",
            {
                "classes": ("wide",),
                "fields": ("username", "phone", "email", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, UserAdmin)
