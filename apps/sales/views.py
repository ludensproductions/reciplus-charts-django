from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.comun.mixins import AutoAccessMixin
from apps.comun.views import (
    GenericCreateFormsetView,
    GenericDeleteView,
    GenericFilterView,
    GenericMultiEntityDetailView,
)
from utils.sequences import get_sequence

from .consts import (
    CHILDREN_ENTITIES,
    CONTEXT_OBJECT_NAME,
    CREATE_TITLE,
    CREATE_URL,
    CUSTOM_BUTTON_TITLE,
    DASHBOARD_URL,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    MOVIE_SALES_FORMSET_CONFIG,
    PERMISSION_ADD,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    QUERY_FIELD,
    TABLE_TITLES,
)
from .filters import SaleFilter
from .forms import BaseASaleFormSet, MovieSalesForm, SaleForm
from .models import Sale


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar ventas."""

    permission_required = PERMISSION_VIEW
    model = Sale
    filterset_class = SaleFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    create_url = CREATE_URL
    # edit_url = EDIT_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    return_url = DASHBOARD_URL
    can_disable = False


class CreateView(PermissionRequiredMixin, GenericCreateFormsetView):
    """Vista para crear nuevas ventas."""

    permission_required = PERMISSION_ADD
    model = Sale
    form_class = SaleForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        """Inicializa la vista configurando el formset de ventas de películas."""
        super().__init__(**kwargs)
        self.formset_config = [
            {
                **MOVIE_SALES_FORMSET_CONFIG,
                "form": MovieSalesForm,
                "base_formset": BaseASaleFormSet,
            },
        ]
        self.create_formset_classes()

    def pre_save(self, form):
        """Asigna el folio y el encargado antes de guardar la venta."""
        main_instance = super().pre_save(form)
        main_instance.folio = get_sequence("sale_sequence")
        main_instance.encargado = self.request.user
        return main_instance

    def post_save(self, main_instance, instances: dict):
        """Calcula el total de la venta después de guardar."""
        movie_sales_instances = instances["movies"]

        total_price = 0
        for movie_sale in movie_sales_instances:
            total_price += movie_sale.movie.price * movie_sale.quantity

        main_instance.total = total_price
        main_instance.save()

        return main_instance

    def get_context_data(self, **kwargs):
        """Obtiene el contexto incluyendo el título personalizado del botón."""
        context = super().get_context_data(**kwargs)
        # Custom button title (if specified it won't grab the title from the view)
        context["custom_button_title"] = CUSTOM_BUTTON_TITLE
        return context


class DeleteView(PermissionRequiredMixin, AutoAccessMixin, GenericDeleteView):
    """Vista para eliminar o deshabilitar ventas."""

    permission_required = PERMISSION_DELETE
    model = Sale
    success_url = reverse_lazy(INDEX_URL)
    can_disable = False
    query = QUERY_FIELD  # <--------- Campo que relaciona al usuario


class DetailView(PermissionRequiredMixin, AutoAccessMixin, GenericMultiEntityDetailView):
    """Vista de detalle para visualizar información de una venta."""

    permission_required = PERMISSION_VIEW
    model = Sale
    context_object_name = CONTEXT_OBJECT_NAME
    title = DETAIL_TITLE
    return_url = INDEX_URL
    query = QUERY_FIELD  # <----------- Campo que relaciona al usuario

    shown_fields = DETAIL_FIELDS
    children_entities = CHILDREN_ENTITIES
    table_title = TABLE_TITLES
