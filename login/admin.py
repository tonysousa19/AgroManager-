from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "nome", "cargo", "is_staff")
    list_filter = ("cargo", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações Pessoais", {"fields": ("nome", "cargo")}),
        (
            "Permissões",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "nome", "cargo", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "nome")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
