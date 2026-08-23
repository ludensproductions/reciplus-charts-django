from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.albums.models import Album, AlbumMerch, Song
from apps.comun.views import (
    GenericCreateFormsetView,
    GenericDeleteView,
    GenericEditFormsetView,
    GenericFilterView,
    GenericMultiEntityDetailView,
)

from .consts import (
    CHILDREN_ENTITIES,
    CONTEXT_OBJECT_NAME,
    CREATE_TITLE,
    CREATE_URL,
    DASHBOARD_URL,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    FILTER_FIELDS,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    MERCH_FORMSET_PREFIX,
    ORDERING,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    SONGS_FORMSET_PREFIX,
    TABLE_TITLES,
)
from .forms import (
    AlbumForm,
    AlbumMerchForm,
    AlbumMerchFormSet,
    AlbumMerchInlineFormSet,
    SongForm,
    SongFormSet,
    SongInlineFormSet,
)


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar álbumes."""

    permission_required = PERMISSION_VIEW
    model = Album
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = ORDERING
    can_disable = True

    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateFormsetView):
    """Vista para crear nuevos álbumes."""

    permission_required = PERMISSION_ADD
    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        """Inicializa la vista configurando los formsets de canciones y merchandise."""
        super().__init__(**kwargs)
        self.formset_config = [
            {
                "title": TABLE_TITLES["songs"],
                "form": SongForm,
                "prefix": SONGS_FORMSET_PREFIX,
                "related_name": "album",
                "base_formset": SongFormSet,
            },
            {
                "title": TABLE_TITLES["merch"],
                "form": AlbumMerchForm,
                "prefix": MERCH_FORMSET_PREFIX,
                "related_name": "album",
                "base_formset": AlbumMerchFormSet,
                "oneToNFormsets": False,
            },
        ]
        self.create_formset_classes()

    def get_context_data(self, **kwargs):
        """Obtiene el contexto incluyendo el título personalizado del botón."""
        context = super().get_context_data(**kwargs)
        # Custom button title (if specified it won't grab the title from the view)
        context["custom_button_title"] = "delete_row"
        return context


class EditView(PermissionRequiredMixin, GenericEditFormsetView):
    """Vista para editar álbumes existentes."""

    permission_required = PERMISSION_CHANGE
    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        """Inicializa la vista configurando los formsets inline de canciones y merchandise."""
        super().__init__(**kwargs)
        self.formset_config = [
            {
                "parent": Album,
                "child": Song,
                "title": TABLE_TITLES["songs"],
                "form": SongForm,
                "prefix": SONGS_FORMSET_PREFIX,
                "related_name": "album",
                "inline_formset": SongInlineFormSet,
            },
            {
                "parent": Album,
                "child": AlbumMerch,
                "title": TABLE_TITLES["merch"],
                "form": AlbumMerchForm,
                "prefix": MERCH_FORMSET_PREFIX,
                "related_name": "album",
                "inline_formset": AlbumMerchInlineFormSet,
            },
        ]
        self.create_formset_classes()

    def get_context_data(self, **kwargs):
        """Obtiene el contexto incluyendo el título personalizado del botón."""
        context = super().get_context_data(**kwargs)
        # Custom button title (if specified it won't grab the title from the view)
        context["custom_button_title"] = "delete_row"
        return context


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar o deshabilitar álbumes."""

    permission_required = PERMISSION_DELETE
    model = Album
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DetailView(PermissionRequiredMixin, GenericMultiEntityDetailView):
    """Vista de detalle para visualizar información de un álbum."""

    permission_required = PERMISSION_VIEW
    model = Album
    context_object_name = CONTEXT_OBJECT_NAME
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    m2m_separator = " | "

    shown_fields = DETAIL_FIELDS
    children_entities = CHILDREN_ENTITIES
    table_title = TABLE_TITLES
