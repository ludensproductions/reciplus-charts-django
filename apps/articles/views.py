from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.comun.consts import ERROR_CONTENT_TYPE_MISMATCH
from apps.comun.views import (
    GenericDeleteView,
    GenericDetailView,
    GenericFilterView,
    GenericUpdateView,
)
from apps.contents.consts import ContentTypes

from .consts import (
    DASHBOARD_URL,
    DEFAULT_ORDERING,
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
    MODEL_NAME,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
)
from .forms import ArticleForm
from .models import Article


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar artículos."""

    permission_required = PERMISSION_VIEW
    model = Article
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    verbose_name = MODEL_NAME.capitalize()
    ordering = DEFAULT_ORDERING
    can_disable = True
    delete_url = DELETE_URL
    edit_url = EDIT_URL
    detail_url = DETAIL_URL
    return_url = DASHBOARD_URL

    def get_queryset(self):
        """Filtra el queryset para mostrar solo artículos."""
        qs = super().get_queryset()
        qs = qs.filter(content__content_type=ContentTypes.ARTICLE)
        return qs


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar artículos existentes."""

    permission_required = PERMISSION_CHANGE
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def get_queryset(self):
        """Filtra el queryset para mostrar solo artículos."""
        qs = super().get_queryset()
        qs = qs.filter(content__content_type=ContentTypes.ARTICLE)
        return qs


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar o deshabilitar artículos."""

    permission_required = PERMISSION_DELETE
    model = Article
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True

    def get_queryset(self):
        """Filtra el queryset para mostrar solo artículos."""
        qs = super().get_queryset()
        qs = qs.filter(content__content_type=ContentTypes.ARTICLE)
        return qs

    def dispatch(self, request, *args, **kwargs):
        """Valida que el artículo pueda ser eliminado antes de procesar la solicitud."""
        self.object: Article = self.get_object()

        if not self.object.should_allow_delete_action():
            messages.error(request, ERROR_CONTENT_TYPE_MISMATCH)
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Maneja las solicitudes POST para eliminar o restaurar artículos."""
        self.object = self.get_object()
        self.is_htmx = request.headers.get("HX-Request", False)
        self.is_delete = True if not self.object.deleted else False

        if self.is_delete:
            return self.delete(request, *args, **kwargs)

        if not self.can_disable:
            return self.handle_response(
                False,
                f"No se puede deshabilitar {self.object}, ya que está deshabilitado.",
            )

        deleted, message = self.object.undelete()
        if self.object.content.deleted:
            self.object.content.undelete()

        return self.handle_response(deleted, message)

    def delete(self, request, *args, **kwargs):
        """Elimina el artículo y su contenido asociado.

        Llama al método delete() del objeto y redirige a la URL de éxito.
        """
        self.object = self.get_object()
        deleted, message = self.object.delete()

        if not self.object.content.deleted:
            self.object.content.delete()

        return self.handle_response(deleted, message)


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Vista de detalle para visualizar información de un artículo."""

    permission_required = PERMISSION_VIEW
    model = Article
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    title = DETAIL_TITLE
    view_deleted_objects = True

    def get_queryset(self):
        """Filtra el queryset para mostrar solo artículos."""
        qs = super().get_queryset()
        qs = qs.filter(content__content_type=ContentTypes.ARTICLE)
        return qs
