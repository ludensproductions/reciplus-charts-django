from django import forms
from simple_history.utils import bulk_create_with_history

from apps.comun.forms import (
    AbstractModelForm,
)
from apps.departments.forms import GroupsWidget
from apps.groups.models import CustomGroup
from apps.positions.models import PositionGroup

from .consts import (
    FORM_DEPARTAMENTO_PLACEHOLDER,
    FORM_GROUPS_LABEL,
    FORM_GROUPS_PLACEHOLDER,
    FORM_PUESTO_LABEL,
    FORM_PUESTO_PLACEHOLDER,
)
from .models import PuestoDepartamento


class PuestoForm(AbstractModelForm):
    """Form for editing a position within a department."""

    departamento = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": FORM_DEPARTAMENTO_PLACEHOLDER,
                "readonly": True,
            }
        ),
    )
    puesto = forms.CharField(
        required=True,
        label=FORM_PUESTO_LABEL,
        max_length=255,
    )

    class Meta:
        model = PuestoDepartamento
        fields = []  # You can change this for the field"s name
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]

        labels = {
            "puesto": FORM_PUESTO_LABEL,
        }

        widgets = {
            "puesto": forms.TextInput(attrs={"placeholder": FORM_PUESTO_PLACEHOLDER}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form and set initial field values."""
        super().__init__(*args, **kwargs)
        # Reorder fields: departamento first.
        new_order = ["departamento", "puesto"]  # Specify desired order
        self.fields = {k: self.fields[k] for k in new_order}
        self.fields["departamento"].disabled = True  # Disable the field to prevent editing.
        self.initial["departamento"] = (
            self.instance.departamento.nombre_departamento if self.instance.departamento else None
        )
        self.initial["puesto"] = self.instance.puesto.puesto if self.instance.puesto else None


class PositionGroupForm(forms.Form):
    """Form for assigning authorization groups to a position."""

    grupos = forms.ModelMultipleChoiceField(
        queryset=CustomGroup.objects.all(),
        widget=GroupsWidget(
            attrs={
                "data-minimum-input-length": "0",
                "class": "form-control",
                "data-allow-clear": "true",
                "data-placeholder": FORM_GROUPS_PLACEHOLDER,
            }
        ),
        required=False,
        label=FORM_GROUPS_LABEL,
    )

    def __init__(self, *args, **kwargs):
        """Initialize the form with the related position-department.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments including `puesto_departamento`.
        """
        self.puesto_departamento = kwargs.pop("puesto_departamento")
        super().__init__(*args, **kwargs)

    def save(self):
        """Persist group assignments for the position.

        Returns:
            list[PositionGroup]: Newly created assignments.
        """
        nuevos_grupos = self.cleaned_data["grupos"]
        nuevos_ids = {grupo.id for grupo in nuevos_grupos}

        # Collect the IDs of groups currently assigned to this position.
        asignaciones_actuales = PositionGroup.objects.filter(puesto_departamento=self.puesto_departamento)
        actuales_ids = set(asignaciones_actuales.values_list("auth_group", flat=True))

        ids_a_eliminar = actuales_ids - nuevos_ids
        ids_a_agregar = nuevos_ids - actuales_ids

        PositionGroup.objects.filter(
            puesto_departamento=self.puesto_departamento, auth_group__in=ids_a_eliminar
        ).delete()

        nuevos_registros = [
            PositionGroup(auth_group=grupo, puesto_departamento=self.puesto_departamento)
            for grupo in nuevos_grupos
            if grupo.id in ids_a_agregar
        ]

        bulk_create_with_history(nuevos_registros, model=PositionGroup)
        return nuevos_registros
