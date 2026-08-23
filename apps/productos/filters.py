from apps.comun.filters import AbstractFilter

from . import consts as productos_consts
from .models import Producto

productos_fields = {
    "producto": {"label": productos_consts.FILTER_PRODUCTO_LABEL},
    "fecha_creacion": {"label": productos_consts.FILTER_FECHA_CREACION_LABEL},
}


class ProductosFilter(AbstractFilter):
    """Filter configuration for productos."""

    class Meta:
        """Metadata for the productos filter set."""

        model = Producto
        fields = list(productos_fields.keys())
        fields_dict = productos_fields
