from apps.comun.filters import AbstractFilter

from . import consts as facturas_consts
from .models import Factura

factura_fields = {
    "codigo_factura": {"label": facturas_consts.FILTER_CODIGO_FACTURA_LABEL},
    "fecha": {"label": facturas_consts.FILTER_FECHA_LABEL},
    "cliente": {"label": facturas_consts.FILTER_CLIENTE_LABEL},
    "total": {"label": facturas_consts.FILTER_TOTAL_LABEL},
}


class FacturaFilter(AbstractFilter):
    """Provide filtering configuration for `Factura` objects.

    Attributes:
        Meta (type): Django FilterSet metadata (model, fields, fields_dict).
    """

    class Meta:
        model = Factura
        fields = list(factura_fields.keys())
        fields_dict = factura_fields
