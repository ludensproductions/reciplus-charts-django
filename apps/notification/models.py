from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.comun.models import AbstractNullableModel
from apps.users.models import User


class Notification(AbstractNullableModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=_("Título"))
    content = models.TextField(max_length=2000, verbose_name=_("Contenido"))
    is_read = models.BooleanField(default=False, verbose_name=_("Leído"))
    notification_type = models.CharField(max_length=255, verbose_name=_("Tipo de notificación"))

    class Meta:
        db_table = "notification"
        verbose_name = _("Notificación")
        verbose_name_plural = _("Notificaciones")
        ordering = ["-id"]

    def __str__(self):
        return self.title
