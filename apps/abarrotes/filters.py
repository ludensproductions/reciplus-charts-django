from apps.comun.filters import AbstractFilter

from .consts import ABARROTES_LABEL, CANTIDAD_LABEL, FECHA_LABEL, PRODUCTO_LABEL
from .models import Abarrotes

abarrotes_fields = {
    "abarrotes": {"label": ABARROTES_LABEL},
    "producto": {"label": PRODUCTO_LABEL},
    "cantidad": {"label": CANTIDAD_LABEL},
    "fecha": {"label": FECHA_LABEL},
}


class AbarrotesFilter(AbstractFilter):
    """Builds filter metadata for abarrotes list views.

    This filter exposes the searchable fields and their localized labels
    used by shared filtering components in the app.
    """

    class Meta:
        model = Abarrotes
        fields = list(abarrotes_fields.keys())
        fields_dict = abarrotes_fields
