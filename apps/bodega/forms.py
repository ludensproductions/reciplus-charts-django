from django import forms
from django.utils.translation import gettext_lazy as _

from apps.comun.forms import AbstractModelForm

from .models import Bodega


class BodegaForm(AbstractModelForm):
    """Form for creating or updating warehouse entries."""

    class Meta:
        model = Bodega
        fields = ["bodega", "producto", "abarrotes", "lote"]
        labels = {
            "bodega": _("Bodega"),
            "producto": _("Producto"),
            "abarrotes": _("Abarrotes"),
            "lote": _("Lote"),
        }

        widgets = {
            "bodega": forms.TextInput(attrs={"placeholder": _("Bodega")}),
            "producto": forms.Select(attrs={"class": "form-control", "placeholder": _("--------")}),
            "abarrotes": forms.Select(attrs={"class": "form-control", "placeholder": _("--------")}),
            "lote": forms.TextInput(attrs={"placeholder": _("Lote")}),
        }
