from apps.comun.filters import AbstractFilter

from .consts import SALE_FILTER_FIELDS
from .models import Sale


class SaleFilter(AbstractFilter):
    """Filter configuration for sale list views."""

    class Meta:
        model = Sale
        fields = list(SALE_FILTER_FIELDS.keys())
        fields_dict = SALE_FILTER_FIELDS
