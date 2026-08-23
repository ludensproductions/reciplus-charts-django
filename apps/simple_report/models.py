from django.db import models
from django.utils.safestring import mark_safe
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.consts import CRUDOperatorsEnum
from apps.comun.models import AbstractModel

from .consts import (
    FIELD_FILE_LABEL,
    FIELD_NOTES_LABEL,
    FIELD_REPORT_LABEL,
    FIELD_TITLE_LABEL,
    MODEL_SIMPLE_REPORT_FILE_NAME,
    MODEL_SIMPLE_REPORT_FILE_NAME_PLURAL,
    MODEL_SIMPLE_REPORT_NAME,
    MODEL_SIMPLE_REPORT_NAME_PLURAL,
)


class SimpleReport(AbstractModel):
    """Store a simple report record with a title and optional notes.

    This model represents a lightweight report entry that can be listed and
    managed through the generic CRUD views.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    title = models.CharField(FIELD_TITLE_LABEL, max_length=100)
    notes = models.TextField(FIELD_NOTES_LABEL, blank=True)

    class Meta:
        db_table = "simple_report"
        verbose_name = MODEL_SIMPLE_REPORT_NAME
        verbose_name_plural = MODEL_SIMPLE_REPORT_NAME_PLURAL
        ordering = ["-id"]

    class Config:
        crud_operations = [
            CRUDOperatorsEnum.INDEX,
            CRUDOperatorsEnum.CREATE,
            CRUDOperatorsEnum.READ,
            CRUDOperatorsEnum.UPDATE,
            CRUDOperatorsEnum.DELETE,
        ]

    def __str__(self):
        """Return the report title for display."""
        # Always return a meaningful value for __str__; use f-strings instead of .format.
        return self.title


class SimpleReportFile(AbstractModel):
    """Store files attached to a simple report.

    Each record references a report and provides a downloadable file.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    report = models.ForeignKey(
        SimpleReport,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name=FIELD_REPORT_LABEL,
    )
    file = models.FileField(FIELD_FILE_LABEL, upload_to="simple_report_files/", blank=False)

    @property
    def get_file_url(self):
        """Return a safe HTML link to the file if it exists, otherwise return an empty string."""
        try:
            if not self.file:
                return ""
            url = getattr(self.file, "url", None)
            name = getattr(self.file, "name", "")
            if url:
                return mark_safe(f'<a href="{url}" target="_blank" rel="noopener" download>{name}</a>')
            return name
        except Exception:
            return ""

    class Meta:
        db_table = "simple_report_file"
        verbose_name = MODEL_SIMPLE_REPORT_FILE_NAME
        verbose_name_plural = MODEL_SIMPLE_REPORT_FILE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return the file name or an empty string if no file is attached."""
        # Always return a meaningful value for __str__; use f-strings instead of .format.
        return self.file.name if self.file else ""
