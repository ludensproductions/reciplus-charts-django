from django import forms
from django.forms import BaseInlineFormSet

from apps.comun.forms import AbstractModelForm, GenericBaseFormSet

from .consts import (
    CANTIDAD_PLACEHOLDER,
    CLIENTE_PLACEHOLDER,
    ERROR_DUPLICATE_PRODUCT,
    PRECIO_UNITARIO_PLACEHOLDER,
    PRODUCTO_PLACEHOLDER,
)
from .models import DetalleFactura, Factura


class FacturaForm(AbstractModelForm):
    """Form for creating and updating `Factura` records."""

    class Meta:
        model = Factura
        fields = ["cliente"]

        widgets = {"cliente": forms.TextInput(attrs={"placeholder": CLIENTE_PLACEHOLDER})}


class DetalleFacturaForm(AbstractModelForm):
    """Form for creating and updating `DetalleFactura` items."""

    class Meta:
        model = DetalleFactura
        fields = ["producto", "cantidad", "precio_unitario"]

        widgets = {
            "producto": forms.TextInput(attrs={"placeholder": PRODUCTO_PLACEHOLDER}),
            "cantidad": forms.NumberInput(attrs={"placeholder": CANTIDAD_PLACEHOLDER}),
            "precio_unitario": forms.NumberInput(attrs={"placeholder": PRECIO_UNITARIO_PLACEHOLDER}),
        }


class DetalleFacturaFormSet(GenericBaseFormSet):
    """Formset to validate `DetalleFactura` entries."""

    def clean(self):
        """Validate the formset data for duplicate products."""
        validate_product(self, self.forms)


class BaseDetalleFacturaInlineFormSet(BaseInlineFormSet):
    """Inline formset to validate `DetalleFactura` entries."""

    def clean(self):
        """Validate the inline formset data for duplicate products."""
        validate_product(self, self.forms)


def validate_product(self, forms):
    """Ensure `producto` is not duplicated within the formset.

    Args:
        self (BaseFormSet): Formset instance invoking validation.
        forms (list[forms.Form]): Forms to validate for duplicates.

    Returns:
        None: This function adds form errors in-place when duplicates are found.
    """
    if any(self.errors):
        # Skip global validation when individual form errors exist.
        return
    productos = []
    for form in forms:
        if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
            producto = form.cleaned_data.get("producto")
            if producto in productos:
                form.add_error("producto", ERROR_DUPLICATE_PRODUCT)
            productos.append(producto)
