from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.utils.text import format_lazy

from apps.comun.consts import ERROR_MIN_LENGTH
from apps.comun.forms import AbstractModelForm

from .consts import VEHICLE_TYPE_LABELS, VEHICLE_TYPE_PLACEHOLDERS
from .models import VehicleType


class VehicleTypeForm(AbstractModelForm):
    """Form to capture the attributes of a vehicle type."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-6 mb-3"),
            ),
        )

    class Meta:
        model = VehicleType
        fields = ["name"]
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]
        labels = VEHICLE_TYPE_LABELS
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": VEHICLE_TYPE_PLACEHOLDERS["name"]}),
        }

    def clean_name(self):
        """Enforce the minimum length for the vehicle type name."""
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise forms.ValidationError(format_lazy(ERROR_MIN_LENGTH, min_length=2))
        return name
