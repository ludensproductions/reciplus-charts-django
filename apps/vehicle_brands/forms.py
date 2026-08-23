from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from apps.comun.consts import ERROR_MIN_LENGTH
from apps.comun.forms import AbstractModelForm

from .models import VehicleBrand


class VehicleBrandForm(AbstractModelForm):
    """Formulario para crear y editar marcas de vehículos."""

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
        """Configuración del modelo y campos del formulario."""

        model = VehicleBrand
        fields = ["name"]
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]
        labels = {
            "name": _("Marca"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": _("Marca")}),
        }

    def clean_name(self):
        """Valida que el nombre tenga al menos 2 caracteres."""
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise forms.ValidationError(format_lazy(ERROR_MIN_LENGTH, min_length=2))
        return name
