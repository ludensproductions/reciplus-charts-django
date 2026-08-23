from django.db.models import BigAutoField
from django.forms.models import fields_for_model

from apps.comun.consts import CRUDOperatorsEnum

from .base_generator import BaseGenerator
from .consts import (
    CONST_CREATE_TITLE,
    CONST_CREATE_URL,
    CONST_DASHBOARD_URL,
    CONST_DEFAULT_ORDERING,
    CONST_DELETE_URL,
    CONST_DETAIL_FIELDS,
    CONST_DETAIL_TITLE,
    CONST_DETAIL_URL,
    CONST_EDIT_TITLE,
    CONST_EDIT_URL,
    CONST_INDEX_FIELDS,
    CONST_INDEX_TITLE,
    CONST_INDEX_URL,
    CONST_PERMISSION_ADD,
    CONST_PERMISSION_CHANGE,
    CONST_PERMISSION_DELETE,
    CONST_PERMISSION_VIEW,
)


class CRUDGenerator(BaseGenerator):
    """Generator for creating CRUD files (views, urls, forms) automatically.

    Generates complete scaffolding for Django CRUD operations including
    views, URL patterns, forms, and filters based on model structure.
    """

    def __init__(self, app_label, model):
        super().__init__(app_label, model)

    def get_fields_formatter(self, fields_to_ignore=(), tab_numbers=2):
        """Formats model fields for use in templates, referencing consts.py LABEL constants.

        Args:
            fields_to_ignore: Tuple of field types to exclude from formatting.
            tab_numbers: Number of indentation levels (default: 2). Each level is 4 spaces.

        Returns:
            Formatted string with field names mapped to their LABEL constant.
        """
        indent = "    " * tab_numbers  # 4 spaces per indentation level
        inner_indent = indent

        # Filter fields excluding ignored types.
        filtered_fields = [field.name for field in self.model_fields if not isinstance(field, fields_to_ignore)]

        lines = [f'"{field}": {self._label_const_name(field)}' for field in filtered_fields]
        result = f",\n{inner_indent}".join(lines)
        # Agregar trailing comma solo al final
        if result:
            result += ","
        return result

    def views(self, operations):
        """Generate CRUD views code for the specified operations.

        Args:
            operations (list[CRUDOperatorsEnum]): CRUD operations to include.

        Returns:
            str: Full content of views.py.
        """
        # Determine which constants are needed based on operations.
        needed_consts = set()

        if CRUDOperatorsEnum.INDEX in operations:
            needed_consts.update(
                [
                    CONST_PERMISSION_VIEW,
                    CONST_INDEX_FIELDS,
                    CONST_INDEX_TITLE,
                    CONST_DEFAULT_ORDERING,
                    CONST_CREATE_URL,
                    CONST_DELETE_URL,
                    CONST_DETAIL_URL,
                    CONST_EDIT_URL,
                    CONST_DASHBOARD_URL,
                ]
            )
        if CRUDOperatorsEnum.CREATE in operations:
            needed_consts.update([CONST_PERMISSION_ADD, CONST_INDEX_URL, CONST_CREATE_TITLE])
        if CRUDOperatorsEnum.UPDATE in operations:
            needed_consts.update([CONST_PERMISSION_CHANGE, CONST_INDEX_URL, CONST_EDIT_TITLE])
        if CRUDOperatorsEnum.DELETE in operations:
            needed_consts.update([CONST_PERMISSION_DELETE, CONST_INDEX_URL])
        if CRUDOperatorsEnum.READ in operations:
            needed_consts.update([CONST_PERMISSION_VIEW, CONST_DETAIL_FIELDS, CONST_INDEX_URL, CONST_DETAIL_TITLE])

        # Generate ordered imports.
        consts_import = ",\n    ".join(sorted(needed_consts))
        if consts_import:
            consts_import += ","

        base_imports = f"""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericDetailView,
    GenericFilterView,
    GenericUpdateView,
)

from .consts import (
    {consts_import}
)
from .filters import {self.module_filter}
from .forms import {self.module_form}
from .models import {self.model_name}
"""

        templates = {
            "index": f'''

class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List view for {self.model_name} with filtering and pagination.

    Displays all active {self.model_name} records with options to create, edit,
    view details, and soft delete. Supports filtering through {self.module_filter}.
    """

    permission_required = PERMISSION_VIEW
    model = {self.model_name}
    filterset_class = {self.module_filter}
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING
    can_disable = True
    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL
''',
            "create": f'''

class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Create view for new {self.model_name} instances.

    Handles the creation of new {self.model_name} records using {self.module_form}.
    """

    permission_required = PERMISSION_ADD
    model = {self.model_name}
    form_class = {self.module_form}
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL
''',
            "update": f'''

class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Update view for existing {self.model_name} instances.

    Allows editing of {self.model_name} records using {self.module_form}.
    """

    permission_required = PERMISSION_CHANGE
    model = {self.model_name}
    form_class = {self.module_form}
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL
''',
            "delete": f'''

class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete view for {self.model_name} instances.

    Handles soft deletion of {self.model_name} records.
    """

    permission_required = PERMISSION_DELETE
    model = {self.model_name}
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True
''',
            "read": f'''

class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Detail view for {self.model_name} instances.

    Displays detailed information for a single {self.model_name} record,
    including soft-deleted records if permitted.
    """

    permission_required = PERMISSION_VIEW
    model = {self.model_name}
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True
''',
        }

        content = base_imports + "".join(templates[op.value] for op in operations if op.value in templates)
        return self._format_code(content)

    def urls(self):
        """Generates the CRUD URLs file.

        Returns:
            String with the complete urls.py code.
        """
        code = """
from django.urls import path

from apps.comun.common_modules_urls import generate_crud_urls

from . import views
from .consts import APP_NAME

app_name = APP_NAME

urlpatterns = generate_crud_urls(views)
"""
        return self._format_code(code)

    def forms(self):
        """Generates the CRUD forms file.

        Creates a ModelForm with all editable fields, proper widgets,
        and user-friendly labels.

        Returns:
            String with the complete forms.py code.
        """
        # Fields included in the generated form.
        field_names = [
            f.name
            for f in self.model_fields
            if getattr(f, "editable", True) and not isinstance(f, self.FIELDS_EXCLUDED_IN_FORMS_AND_LABELS)
        ]

        # Resolve FormFields using Django's internal logic.
        ff_by_name = fields_for_model(self.model, fields=field_names)

        # Build 'name': forms.WidgetClass() lines using Django's widget class names.
        # Placeholders reference the field's LABEL constant from consts.py so the
        # translated text stays centralized instead of being duplicated here.
        widget_lines = []
        for name in ff_by_name:
            widget_cls = ff_by_name[name].widget.__class__.__name__
            widget_lines.append(
                f'"{name}": forms.{widget_cls}(attrs={{"placeholder": {self._label_const_name(name)}}})'
            )
        widgets_block = ",\n            ".join(widget_lines)
        # Agregar trailing comma solo al final
        if widgets_block:
            widgets_block += ","

        labels = self.get_fields_formatter(self.FIELDS_EXCLUDED_IN_FORMS_AND_LABELS, 3)

        # Obtener campos para el formulario
        form_field_names = [field.name for field in self.model_fields if not isinstance(field, BigAutoField)]
        fields_str = self._format_fields_list(form_field_names)

        label_imports = sorted({self._label_const_name(field.name) for field in self._labelable_fields()})
        consts_import_block = ""
        if label_imports:
            imports_joined = ",\n    ".join(label_imports)
            consts_import_block = f"\nfrom .consts import (\n    {imports_joined},\n)"

        code = f'''
from django import forms

from apps.comun.forms import AbstractModelForm
{consts_import_block}
from .models import {self.model_name}


class {self.model_name}Form(AbstractModelForm):
    """Form for creating and editing {self.model_name} instances.

    Provides widgets and labels for all editable fields with
    user-friendly placeholders.
    """

    class Meta:
        model = {self.model_name}
        fields = {fields_str}
        labels = {{
            {labels}
        }}

        widgets = {{
            {widgets_block}
        }}
'''
        return self._format_code(code)
