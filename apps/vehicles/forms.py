from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.utils.text import format_lazy

from apps.comun.consts import ERROR_MIN_LENGTH
from apps.comun.forms import AbstractModelForm

from .const import (
    ERROR_INVALID_YEAR,
    VEHICLE_LABELS,
    VEHICLE_PLACEHOLDERS,
)
from .models import Vehicle


class VehicleForm(AbstractModelForm):
    """Form for creating or updating a vehicle."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-4 mb-3"),
                Column("brand", css_class="form-group col-md-4 mb-3"),
                Column("vehicle_type", css_class="form-group col-md-4 mb-3"),
                Column("license_plate", css_class="form-group col-md-4 mb-3"),
                Column("year", css_class="form-group col-md-4 mb-3"),
                Column("model", css_class="form-group col-md-4 mb-3"),
            ),
        )

    class Meta:
        model = Vehicle
        fields = ["name", "brand", "vehicle_type", "license_plate", "year", "model"]
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]
        labels = VEHICLE_LABELS
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": VEHICLE_PLACEHOLDERS["name"]}),
            "brand": forms.Select(attrs={"placeholder": VEHICLE_PLACEHOLDERS["brand"]}),
            "vehicle_type": forms.Select(attrs={"placeholder": VEHICLE_PLACEHOLDERS["vehicle_type"]}),
            "license_plate": forms.TextInput(attrs={"placeholder": VEHICLE_PLACEHOLDERS["license_plate"]}),
            "year": forms.NumberInput(attrs={"placeholder": VEHICLE_PLACEHOLDERS["year"]}),
            "model": forms.TextInput(attrs={"placeholder": VEHICLE_PLACEHOLDERS["model"]}),
        }

    def clean_name(self):
        """Ensure the vehicle name meets the minimum length requirement."""
        name = self.cleaned_data.get("name")
        if name and len(name) < 2:
            raise forms.ValidationError(format_lazy(ERROR_MIN_LENGTH, min_length=2))
        return name

    def clean_license_plate(self):
        """Ensure the license plate is long enough."""
        plate = self.cleaned_data.get("license_plate")
        if plate and len(plate) < 4:
            raise forms.ValidationError(format_lazy(ERROR_MIN_LENGTH, min_length=4))
        return plate

    def clean_year(self):
        """Ensure the year is within the allowed range."""
        year = self.cleaned_data.get("year")
        if year is not None and (year < 1900 or year > 2100):
            raise forms.ValidationError(ERROR_INVALID_YEAR)
        return year

    def clean_model(self):
        """Ensure the model name is not empty."""
        model = self.cleaned_data.get("model")
        if model and len(model) < 1:
            raise forms.ValidationError(format_lazy(ERROR_MIN_LENGTH, min_length=1))
        return model
