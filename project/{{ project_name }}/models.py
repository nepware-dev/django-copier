from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class UserStampedModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("created by"),
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("updated by"),
    )

    class Meta:
        abstract = True


class UpdateFieldsMixin:
    def save(self, *args, **kwargs):
        if self.pk:
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    old_val = getattr(old, field_name)
                    new_val = getattr(self, field_name)
                    if hasattr(field, "is_custom_lower_field"):
                        if field.is_custom_lower_field():
                            new_val = new_val.lower()
                    if old_val != new_val:
                        changed_fields.append(field_name)
                except Exception:
                    pass
            kwargs["update_fields"] = changed_fields
        super().save(*args, **kwargs)