from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.comun.models import AbstractModel
from apps.comun.validators import unicode_letter_validator


class Abarrotes(AbstractModel):
    abarrotes = models.CharField(max_length=100, validators=[unicode_letter_validator], verbose_name=_("Abarrotes"))
    producto = models.ForeignKey(
        "productos.Producto",
        related_query_name="producto_abarrotes",
        related_name="abarrotes_productos",
        on_delete=models.CASCADE,
        verbose_name=_("Producto"),
    )
    cantidad = models.PositiveIntegerField(verbose_name=_("Cantidad"))
    fecha = models.DateField(verbose_name=_("Fecha"))

    class Meta:
        db_table = "abarrotes"
        verbose_name = _("Abarrote")
        verbose_name_plural = _("Abarrotes")
        ordering = ["-id"]

    def __str__(self):
        return self.abarrotes
