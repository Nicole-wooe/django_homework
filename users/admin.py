from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "phone",
        "country",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "country",
    )
    search_fields = (
        "email",
        "phone",
        "country",
    )
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личная информация", {"fields": ("avatar", "phone", "country")}),
        ("Права доступа", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )
