from django.db import models

from apps.comun.models import AbstractModel
from apps.productos import consts as productos_consts


class Producto(AbstractModel):
    """Represent a product entry linked to a product type.

    This model stores product names, their associated type, and the creation
    date. It also defines relationships that govern cascading deletes.

    Attributes:
        producto (str): Product name.
        tipo_producto (TipoProducto): Product type reference.
        fecha_creacion (date): Creation date.
    """

    producto = models.TextField(unique=True, verbose_name=productos_consts.PRODUCTO_LABEL)
    tipo_producto = models.ForeignKey(
        "tipo_productos.TipoProducto",
        on_delete=models.CASCADE,
        related_name="tipo_productos",
        related_query_name="tipo_producto",
        verbose_name=productos_consts.TIPO_PRODUCTO_LABEL,
    )
    fecha_creacion = models.DateField(verbose_name=productos_consts.FECHA_CREACION_LABEL)

    delete_on_cascade = [
        "producto_abarrotes",
        "bodega_producto",
    ]

    # Relations that prevent delete/restore when related objects are present.
    parent_relations = [("tipo productos", "tipo_producto", "productos:index")]
    child_relations = [("abarrotes", "producto_abarrotes", "abarrotes:index")]

    class Meta:
        db_table = "producto"
        verbose_name = productos_consts.PRODUCTO_VERBOSE_NAME
        verbose_name_plural = productos_consts.PRODUCTO_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return the product name.

        Returns:
            str: Product name.
        """
        return self.producto
