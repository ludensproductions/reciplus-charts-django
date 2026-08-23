from django.utils.translation import gettext_lazy as _

from apps.comun.filters import AbstractFilter

from .models import Bodega

bodega_fields = {
    "bodega": {"label": _("Bodega")},
    "producto": {"label": _("Producto")},
    "abarrotes": {"label": _("Abarrotes")},
    "lote": {"label": _("Lote")},
}


class BodegaFilter(AbstractFilter):
    """Filter set for warehouse records."""

    class Meta:
        model = Bodega
        fields = list(bodega_fields.keys())
        fields_dict = bodega_fields
