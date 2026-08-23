from django import forms
from django.utils.translation import gettext_lazy as _

from apps.comun.forms import AbstractModelForm

from .models import TipoProducto

FIELD_PRODUCT_TYPE_LABEL = _("Nombre tipo producto")
FIELD_PRODUCT_TYPE_PLACEHOLDER = _("Tipo de producto")


class TipoProductoForm(AbstractModelForm):
    """Form to create or update product types.

    This form exposes the `nombre` field with a localized label and placeholder
    used in the UI.
    """

    class Meta:
        model = TipoProducto
        fields = ["nombre"]
        labels = {
            "nombre": FIELD_PRODUCT_TYPE_LABEL,
        }

        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": FIELD_PRODUCT_TYPE_PLACEHOLDER}),
        }
