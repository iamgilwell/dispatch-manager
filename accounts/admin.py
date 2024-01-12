from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import UserProfile

User = get_user_model()

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "role",
        "active",
        "staff",
        "admin",
    )
    list_selected_related = True
    list_filter = ("admin",)
    fieldsets = (
        (
            "USER NAMES,EMAIL & PASSWORD",
            {
                "fields": ( "first_name",
                    "last_name","email", "password"),
            },
        ),
        (
            "WORK PROFILE",
            {
                "fields": (
                    "role",
                    "staff_id",
                )
            },
        ),
        (
            "PERMISSIONS",
            {
                "fields": (
                    "admin",
                    "staff",
                    "active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "USER DETAILS",
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "admin",
                    "staff",
                    "active",
                ),
            },
        ),
        (
            "WORK PROFILE",
            {
                "classes": ("wide",),
                "fields": (
                    "role",
                    "staff_id",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, UserAdmin)
