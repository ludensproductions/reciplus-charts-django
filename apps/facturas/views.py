import uuid

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.comun.views import (
    GenericCreateFormsetView,
    GenericDeleteView,
    GenericEditFormsetView,
    GenericFilterView,
    GenericMultiEntityDetailView,
)

from .consts import (
    CREATE_TITLE,
    CREATE_URL,
    DASHBOARD_URL,
    DEFAULT_ORDERING,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    FACTURA_DETAIL_FORMSET_PREFIX,
    FACTURA_DETAIL_FORMSET_TITLE,
    FACTURA_DETAIL_RELATED_NAME,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    TABLE_DETAIL_FIELDS,
    TABLE_TITLES,
)
from .filters import FacturaFilter
from .forms import BaseDetalleFacturaInlineFormSet, DetalleFacturaForm, DetalleFacturaFormSet, FacturaForm
from .models import DetalleFactura, Factura


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Display the factura list with filtering and actions.

    Attributes:
        permission_required (str): Permission codename required to access the view.
        model (type): Model class used by the view.
        filterset_class (type): FilterSet class for filtering querysets.
        shown_fields (list[str]): Field names shown in the list view.
        title (str): Page title for the view.
        ordering (list[str]): Default ordering for the queryset.
        can_disable (bool): Whether records can be disabled from the list.
        create_url (str): URL name for creating a factura.
        delete_url (str): URL name for deleting a factura.
        detail_url (str): URL name for viewing a factura.
        edit_url (str): URL name for updating a factura.
        return_url (str): URL name for returning to the dashboard.
    """

    permission_required = PERMISSION_VIEW
    model = Factura
    filterset_class = FacturaFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING
    can_disable = True
    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateFormsetView):
    """Create a factura and its detail items using formsets.

    Attributes:
        permission_required (str): Permission codename required to access the view.
        model (type): Model class used by the view.
        form_class (type): Form class for the main factura.
        success_url (str): URL to redirect to after a successful create.
        title (str): Page title for the view.
        return_url (str): URL name for returning to the list view.
        formset_config (list[dict]): Configuration for child formsets.
    """

    permission_required = PERMISSION_ADD
    model = Factura
    form_class = FacturaForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        """Initialize the view and configure the formsets.

        Args:
            **kwargs: Keyword arguments passed to the parent initializer.
        """
        super().__init__(**kwargs)
        self.formset_config = [
            {
                "title": FACTURA_DETAIL_FORMSET_TITLE,
                "form": DetalleFacturaForm,
                "prefix": FACTURA_DETAIL_FORMSET_PREFIX,
                "related_name": FACTURA_DETAIL_RELATED_NAME,
                "base_formset": DetalleFacturaFormSet,
            },
        ]
        self.create_formset_classes()

    def pre_save(self, form):
        """Prepare the factura before saving.

        Args:
            form (forms.ModelForm): Main factura form.

        Returns:
            Factura: Prepared factura instance.
        """
        instance = super().pre_save(form)

        if not instance.codigo_factura:
            instance.codigo_factura = str(uuid.uuid4()).replace("-", "")[:8]

        instance.created_by = self.request.user
        return instance

    def post_save(self, main_instance, instances):
        """Update the factura total after saving formsets.

        Args:
            main_instance (Factura): Persisted factura instance.
            instances (dict[str, list]): Saved formset instances keyed by prefix.

        Returns:
            Factura: Updated factura instance.
        """
        detalles = instances.get("detalle", [])
        total = 0

        for detalle in detalles:
            total += detalle.subtotal

        main_instance.total = total
        main_instance.save()

        return main_instance

    def process_formset_instance(self, child_form_instance, formset_config, main_instance):
        """Prepare a detail instance before saving.

        Args:
            child_form_instance (DetalleFactura): Detail instance to prepare.
            formset_config (dict): Formset configuration metadata.
            main_instance (Factura): Parent factura instance.

        Returns:
            DetalleFactura: Prepared detail instance.
        """
        child_form_instance.factura = main_instance
        child_form_instance.subtotal = child_form_instance.cantidad * child_form_instance.precio_unitario
        child_form_instance.codigo_detalle = (
            f"{main_instance.codigo_factura}-"
            f"{child_form_instance.producto[:3].upper()}-"
            f"{child_form_instance.cantidad}-"
            f"{uuid.uuid4().hex[:4]}"
        )
        return child_form_instance


class DetailView(PermissionRequiredMixin, GenericMultiEntityDetailView):
    """Show factura details along with its related detail items.

    Attributes:
        permission_required (str): Permission codename required to access the view.
        model (type): Model class used by the view.
        shown_fields (list[str]): Field names shown in the detail view.
        return_url (str): URL name for returning to the list view.
        success_url (str): URL to redirect to after a successful action.
        title (str): Page title for the view.
        view_deleted_objects (bool): Whether to include disabled records.
        children_entities (dict): Mapping of related entities for display.
        table_title (dict): Table titles for related entity sections.
    """

    permission_required = PERMISSION_VIEW
    model = Factura
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True
    children_entities = TABLE_DETAIL_FIELDS
    table_title = TABLE_TITLES


class EditView(PermissionRequiredMixin, GenericEditFormsetView):
    """Edit a factura and its detail items using formsets.

    Attributes:
        permission_required (str): Permission codename required to access the view.
        model (type): Model class used by the view.
        form_class (type): Form class for the main factura.
        success_url (str): URL to redirect to after a successful update.
        title (str): Page title for the view.
        return_url (str): URL name for returning to the list view.
        formset_config (list[dict]): Configuration for child formsets.
    """

    permission_required = PERMISSION_CHANGE
    model = Factura
    form_class = FacturaForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        """Initialize the view and configure the inline formsets.

        Args:
            **kwargs: Keyword arguments passed to the parent initializer.
        """
        super().__init__(**kwargs)
        self.formset_config = [
            {
                "parent": Factura,
                "child": DetalleFactura,
                "title": FACTURA_DETAIL_FORMSET_TITLE,
                "form": DetalleFacturaForm,
                "prefix": FACTURA_DETAIL_FORMSET_PREFIX,  # Prefijo único para los campos del formset en el HTML.
                "related_name": FACTURA_DETAIL_RELATED_NAME,  # Nombre de la relación en el modelo `DetalleFactura
                "inline_formset": BaseDetalleFacturaInlineFormSet,  # Se usa un formset inline para editar los detalles
            }
        ]
        self.create_formset_classes()

    def post_save(self, main_instance, instances, edited_instances):
        """Recalculate the factura total after editing detail items.

        Args:
            main_instance (Factura): Persisted factura instance.
            instances (dict[str, list]): New formset instances keyed by prefix.
            edited_instances (dict[str, list]): Edited instances keyed by prefix.

        Returns:
            Factura: Updated factura instance.
        """
        for detalle in main_instance.detalles.all():
            if detalle.cantidad and detalle.precio_unitario:
                detalle.subtotal = detalle.cantidad * detalle.precio_unitario
                detalle.save()

        total = sum(detalle.subtotal for detalle in main_instance.detalles.all())
        main_instance.total = total
        main_instance.save()

        return main_instance

    def process_formset_instance(self, child_form_instance, formset_config, main_instance):
        """Prepare a detail instance before saving.

        Args:
            child_form_instance (DetalleFactura): Detail instance to prepare.
            formset_config (dict): Formset configuration metadata.
            main_instance (Factura): Parent factura instance.

        Returns:
            DetalleFactura: Prepared detail instance.
        """
        child_form_instance.factura = main_instance
        if child_form_instance.cantidad and child_form_instance.precio_unitario:
            child_form_instance.subtotal = child_form_instance.cantidad * child_form_instance.precio_unitario
            child_form_instance.codigo_detalle = (
                f"{main_instance.codigo_factura}-"
                f"{child_form_instance.producto[:3].upper()}-"
                f"{child_form_instance.cantidad}-"
                f"{uuid.uuid4().hex[:4]}"
            )
        return child_form_instance


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Disable or delete a factura based on permissions.

    Attributes:
        permission_required (str): Permission codename required to access the view.
        model (type): Model class used by the view.
        success_url (str): URL to redirect to after a successful delete.
        can_disable (bool): Whether the view supports soft-disable actions.
    """

    permission_required = PERMISSION_DELETE
    model = Factura
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True
