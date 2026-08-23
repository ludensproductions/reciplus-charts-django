from django.utils.translation import gettext_lazy as _

from apps.comun.filters import AbstractFilter

from .models import TipoProducto

tipo_productos_fields = {
    "nombre": {"label": _("Tipo producto")},
}


class TipoProductosFilter(AbstractFilter):
    class Meta:
        model = TipoProducto
        fields = list(tipo_productos_fields.keys())
        fields_dict = tipo_productos_fields
