from django import forms

from apps.comun.forms import AbstractModelForm

from . import consts as productos_consts
from .models import Producto


class ProductoForm(AbstractModelForm):
    """Form for creating and updating productos."""

    class Meta:
        model = Producto
        fields = ["producto", "tipo_producto", "fecha_creacion"]
        labels = {
            "producto": productos_consts.FORM_PRODUCTO_LABEL,
            "tipo_producto": productos_consts.FORM_TIPO_PRODUCTO_LABEL,
            "fecha_creacion": productos_consts.FORM_FECHA_CREACION_LABEL,
        }

        widgets = {
            "producto": forms.TextInput(attrs={"placeholder": productos_consts.FORM_PRODUCTO_PLACEHOLDER}),
            "tipo_producto": forms.Select(
                attrs={"class": "form-control", "placeholder": productos_consts.FORM_TIPO_PRODUCTO_PLACEHOLDER}
            ),
            "fecha_creacion": forms.DateTimeInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
