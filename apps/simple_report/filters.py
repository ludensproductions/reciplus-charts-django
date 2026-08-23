from apps.comun.filters import AbstractFilter

from .consts import SIMPLE_REPORT_FILTER_FIELDS
from .models import SimpleReport


class SimpleReportFilter(AbstractFilter):
    """Filter configuration for simple report list views."""

    class Meta:
        model = SimpleReport
        fields = list(SIMPLE_REPORT_FILTER_FIELDS.keys())
        fields_dict = SIMPLE_REPORT_FILTER_FIELDS
