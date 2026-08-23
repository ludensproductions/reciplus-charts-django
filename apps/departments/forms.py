from crispy_forms.helper import FormHelper
from django import forms

from apps.comun.forms import (
    AbstractModelForm,
    GenericBaseFormSet,
    GenericBaseInlineFormSet,
)
from apps.comun.select2.widgets import BaseModelSelect2MultipleWidget, ModelSelect2SingleTagWidget
from apps.groups.models import CustomGroup
from apps.positions.models import Puesto, PuestoDepartamento

from . import consts as departments_consts
from .consts import ERROR_AT_LEAST_ONE_BOSS, ERROR_BOSS_REQUIRED, ERROR_SINGLE_BOSS
from .models import Departamento


class PositionTagWidget(ModelSelect2SingleTagWidget):
    """Select2 widget that allows creating or selecting positions."""

    model = Puesto
    queryset = Puesto.objects.all().order_by("puesto")
    search_fields = ["puesto__icontains"]

    def __init__(self, *args, **kwargs):
        """Configure the widget data source."""
        kwargs["data_view"] = "departments:position_select2"
        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        """Return a display label for a position.

        Args:
            obj (Puesto): Position instance.

        Returns:
            str: Position label.
        """
        return obj.puesto

    def value_from_datadict(self, data, files, name):
        """Create objects for non-primary values and return the PK.

        Args:
            data (dict): Submitted data.
            files (dict): Uploaded files.
            name (str): Field name.

        Returns:
            str | None: Primary key string or None when empty.
        """
        value = super().value_from_datadict(data, files, name)

        # Validate the value before processing
        if not value:
            return None

        # If the value is already an integer (PK), just return it
        try:
            pk = int(value)
            if self.queryset.filter(pk=pk).exists():
                return value  # It's an existing PK
        except (ValueError, TypeError):
            pass  # Not an int, so proceed to the next check

        # If it's not a valid PK, check if the value already exists as a name
        existing = self.queryset.filter(puesto__iexact=value).first()
        if existing:
            return str(existing.pk)  # Return the existing PK to avoid duplicates

        # If it's a new value, create a new `Puesto`
        new_instance = self.queryset.create(puesto=value)
        return str(new_instance.pk)


class DepartmentForm(AbstractModelForm):
    """Form for creating or updating departments."""

    class Meta:
        model = Departamento
        fields = ["nombre_departamento", "departamento_superior"]
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]

        labels = {
            "nombre_departamento": departments_consts.DEPARTMENT_NAME_LABEL,
            "departamento_superior": departments_consts.PARENT_DEPARTMENT_LABEL,
        }

        widgets = {
            "nombre_departamento": forms.TextInput(
                attrs={"placeholder": departments_consts.DEPARTMENT_NAME_PLACEHOLDER}
            ),
            "departamento_superior": forms.Select(),
        }


class PositionForm(AbstractModelForm):
    """Form for assigning positions within a department."""

    class Meta:
        model = PuestoDepartamento
        fields = ["puesto", "jefe_departamento"]
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]

        labels = {
            "puesto": departments_consts.POSITION_LABEL,
            "jefe_departamento": departments_consts.IS_DEPARTMENT_HEAD_LABEL,
        }

        widgets = {
            "puesto": PositionTagWidget(
                attrs={
                    "class": "form-control",
                    "data-allow-clear": "true",
                    "data-placeholder": departments_consts.EMPTY_SELECT_PLACEHOLDER,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form helper for inline layouts."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


class PositionInlineFormSet(GenericBaseInlineFormSet):
    """Inline formset enforcing a single department boss."""

    def clean(self):
        """Validate that one and only one boss is selected.

        Raises:
            ValidationError: When none or more than one boss is selected.
        """
        super().clean()
        jefes = [form.cleaned_data["jefe_departamento"] for form in self.forms]

        if not any(jefes):
            raise forms.ValidationError(ERROR_AT_LEAST_ONE_BOSS)

        cont_jefes = jefes.count(True)

        if cont_jefes > 1:
            raise forms.ValidationError(ERROR_SINGLE_BOSS)


class PositionFormSet(GenericBaseFormSet):
    """Formset enforcing a single department boss."""

    def clean(self):
        """Validate that one and only one boss is selected.

        Raises:
            ValidationError: When none or more than one boss is selected.
        """
        super().clean()

        jefes = [form.cleaned_data["jefe_departamento"] for form in self.forms]

        if not any(jefes):
            raise forms.ValidationError(ERROR_BOSS_REQUIRED)

        cont_jefes = jefes.count(True)
        if cont_jefes > 1:
            raise forms.ValidationError(ERROR_SINGLE_BOSS)


class GroupsWidget(BaseModelSelect2MultipleWidget):
    """Select2 widget for authorization groups."""

    model = CustomGroup
    queryset = CustomGroup.objects.all()
    search_fields = ["display_name__icontains"]


class GruposDepartamentoForm(forms.Form):
    """Form for assigning groups to a department."""

    auth_group = forms.ModelMultipleChoiceField(
        queryset=CustomGroup.objects.all(),
        label=departments_consts.GROUPS_LABEL,
        required=False,
        widget=GroupsWidget(
            attrs={
                "data-minimum-input-length": "0",
                "class": "form-control",
                "data-allow-clear": "true",
                "data-placeholder": departments_consts.EMPTY_SELECT_PLACEHOLDER,
            }
        ),
    )
