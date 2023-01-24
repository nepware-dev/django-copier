from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User

ADDITIONAL_FIELDS = tuple()

ADDITIONAL_USER_FIELDSETS = (
    (
        _("Additional Fields"),
        {"fields": ADDITIONAL_FIELDS},
    ),
)


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDSETS
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                ) + ADDITIONAL_FIELDS + (
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
