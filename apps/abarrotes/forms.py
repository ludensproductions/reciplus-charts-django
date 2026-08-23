"""Form definitions for the abarrotes app."""

from django import forms

from apps.comun.forms import AbstractModelForm

from .consts import (
    ABARROTES_LABEL,
    CANTIDAD_LABEL,
    FECHA_LABEL,
    PRODUCTO_LABEL,
    SELECT_EMPTY_PLACEHOLDER,
)
from .models import Abarrotes


class AbarrotesForm(AbstractModelForm):
    """Manages create and update operations for abarrotes records.

    This form centralizes localized labels and widget configuration for
    inventory entries in the abarrotes domain.
    """

    class Meta:
        """Configuration for model binding and field presentation."""

        model = Abarrotes
        fields = ["abarrotes", "producto", "cantidad", "fecha"]
        labels = {
            "abarrotes": ABARROTES_LABEL,
            "producto": PRODUCTO_LABEL,
            "cantidad": CANTIDAD_LABEL,
            "fecha": FECHA_LABEL,
        }

        widgets = {
            "abarrotes": forms.TextInput(attrs={"class": "form-control"}),
            "producto": forms.Select(attrs={"placeholder": SELECT_EMPTY_PLACEHOLDER}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": 1}),
            "fecha": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
