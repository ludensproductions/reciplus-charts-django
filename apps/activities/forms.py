from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django_select2 import forms as s2forms

from apps.comun.consts import ERROR_MIN_LENGTH
from apps.comun.forms import AbstractModelForm

from .models import Activity


class ActivityForm(AbstractModelForm):
    """Form for creating and editing Activity instances with Select2 widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-4 mb-3"),
                Column("location", css_class="form-group col-md-4 mb-3"),
                Column("activity_type", css_class="form-group col-md-4 mb-3"),
            ),
        )

    class Meta:
        """Meta configuration for ActivityForm."""

        model = Activity
        fields = ["name", "location", "activity_type"]
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]
        labels = {
            "name": _("Nombre"),
            "location": _("Ubicación"),
            "activity_type": _("Tipo de actividad"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": _("Nombre de la actividad")}),
            "location": forms.TextInput(attrs={"placeholder": _("Ubicación")}),
            "activity_type": s2forms.Select2Widget(attrs={"data-theme": "bootstrap-5"}),
        }

    def clean_name(self):
        """Validate that activity name has at least 3 characters.

        Returns:
            str: Cleaned name value.

        Raises:
            forms.ValidationError: If name is shorter than 3 characters.
        """
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise forms.ValidationError(format_lazy(ERROR_MIN_LENGTH, min_length=3))
        return name
