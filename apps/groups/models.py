from django.contrib.auth.models import Group
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from safedelete.managers import (
    SafeDeleteAllManager,
    SafeDeleteDeletedManager,
    SafeDeleteManager,
)
from safedelete.models import SOFT_DELETE

from apps.comun.models import AbstractNullableModel


class CustomGroup(Group, AbstractNullableModel):
    _safedelete_policy = SOFT_DELETE
    display_name = CharField(max_length=150)

    objects = SafeDeleteManager()
    deleted_objects = SafeDeleteDeletedManager()
    all_objects = SafeDeleteAllManager()

    class Meta:
        db_table = "groups"
        verbose_name = _("Grupo")
        verbose_name_plural = _("Grupos")
        ordering = ["id"]

    def __str__(self):
        return self.display_name
