from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.comun.fields import DisplayNameField
from apps.comun.models import AbstractModel

FIELD_NAME_LABEL = _("Nombre")
MODEL_VERBOSE_NAME = _("Tipo de producto")
MODEL_VERBOSE_NAME_PLURAL = _("Tipos de producto")


class TipoProducto(AbstractModel):
    """Store a product type used to classify products in the catalog.

    This model represents a business category that groups products under a
    shared type name. The name must be unique per record and is used as the
    human-readable label across the application.
    """

    nombre = models.CharField(FIELD_NAME_LABEL, max_length=255)
    display_name = DisplayNameField(
        verbose_name=FIELD_NAME_LABEL,
        display_name="nombre",
        max_length=255,
    )

    child_relations = [
        ("producto", "tipo_producto", "productos:index"),
    ]

    class Meta:
        db_table = "tipo_producto"
        verbose_name = MODEL_VERBOSE_NAME
        verbose_name_plural = MODEL_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return the display name for the product type.

        Returns:
            str: Product type name.
        """
        return self.nombre
