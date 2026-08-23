from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms

from apps.comun.fields import MultiFileField
from apps.comun.forms import AbstractModelForm
from apps.comun.widgets import MultiFileInput

from .consts import (
    FIELD_FILES_LABEL,
    FIELD_FILES_PLACEHOLDER,
    FIELD_NOTES_LABEL,
    FIELD_NOTES_PLACEHOLDER,
    FIELD_TITLE_LABEL,
    FIELD_TITLE_PLACEHOLDER,
)
from .models import SimpleReport


class SimpleReportForm(AbstractModelForm):
    """Form to create or update simple reports with optional file uploads."""

    files = MultiFileField(
        label=FIELD_FILES_LABEL,
        required=False,
        widget=MultiFileInput(attrs={"multiple": "multiple", "placeholder": FIELD_FILES_PLACEHOLDER}),
    )

    class Meta:
        model = SimpleReport
        fields = ["title", "notes"]
        labels = {"title": FIELD_TITLE_LABEL, "notes": FIELD_NOTES_LABEL}

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": FIELD_TITLE_PLACEHOLDER}),
            "notes": forms.Textarea(attrs={"placeholder": FIELD_NOTES_PLACEHOLDER}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="form-group col-md-12 mb-3"),
            ),
            Row(
                Column("notes", css_class="form-group col-12 mb-3"),
            ),
            Row(
                Column("files", css_class="col-12 mb-3"),
            ),
        )
