from django.contrib.postgres.forms import RangeWidget as DjangoRangeWidget
from django.forms import ClearableFileInput, FileInput


class RangeWidget(DjangoRangeWidget):
    """Custom range widget using a specific template."""

    template_name = "comun/range_widget.html"


class MultiFileInput(FileInput):
    """File input widget that allows multiple file selection."""

    allow_multiple_selected = True


class ClearableMultiFileInput(ClearableFileInput):
    """Clearable file input widget that allows multiple file selection."""

    allow_multiple_selected = True
