from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("user_id","email","nickname","name","is_active","is_staff","is_admin","last_login")
    search_fields = ("email","nickname","name","phone_number")
    list_filter = ("is_staff", "is_active")
    readonly_fields = ("is_admin",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("개인 정보", {"fields": ("nickname", "name", "phone_number")}),
        ("권한", {"fields": ("is_active", "is_staff", "is_admin", "is_superuser", "groups", "user_permissions")}),
        ("로그", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nickname", "name", "phone_number", "password1", "password2", "is_active", "is_staff", "is_admin"),
        }),
    )