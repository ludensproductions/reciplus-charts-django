import json
import mimetypes

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericFilterView,
    GenericMultiEntityDetailView,
    GenericUpdateView,
)

from .consts import (
    CHILDREN_ENTITIES,
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
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    TABLE_TITLES,
)
from .filters import SimpleReportFilter
from .forms import SimpleReportForm
from .models import SimpleReport, SimpleReportFile


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar reportes simples."""

    permission_required = PERMISSION_VIEW
    model = SimpleReport
    filterset_class = SimpleReportFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING
    can_disable = True
    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Vista para crear nuevos reportes simples."""

    permission_required = PERMISSION_ADD
    template_name = "simple_report/form.html"
    model = SimpleReport
    form_class = SimpleReportForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL

    def get_context_data(self, **kwargs):
        """Obtiene el contexto inicializando file_urls como array vacío."""
        context = super().get_context_data(**kwargs)
        # Ensure template JS has an array for create view
        context["file_urls"] = []
        return context

    @transaction.atomic
    def form_valid(self, form):
        """Procesa el formulario válido guardando el reporte y sus archivos."""
        self.object = form.save()

        # Save files
        if form.cleaned_data.get("files"):
            for file in form.cleaned_data["files"]:
                SimpleReportFile.objects.create(report=self.object, file=file, created_by=self.request.user)

        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)

        return HttpResponseRedirect(self.get_success_url())


class DetailView(PermissionRequiredMixin, GenericMultiEntityDetailView):
    """Vista de detalle para visualizar información de un reporte simple."""

    permission_required = PERMISSION_VIEW
    model = SimpleReport
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True
    children_entities = CHILDREN_ENTITIES
    table_title = TABLE_TITLES


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar reportes simples existentes."""

    permission_required = PERMISSION_CHANGE
    template_name = "simple_report/form.html"
    model = SimpleReport
    form_class = SimpleReportForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def get_context_data(self, **kwargs):
        """Obtiene el contexto incluyendo metadatos de archivos para FilePond."""
        context = super().get_context_data(**kwargs)

        # Provide file metadata for FilePond preloading (id, url, name)
        files_data = []
        for file in self.object.files.all():
            # Get content type from file field or guess from extension
            content_type = None
            try:
                # Try to get content type from the file field
                if hasattr(file.file, "content_type") and file.file.content_type:
                    content_type = file.file.content_type
                else:
                    # Fallback: guess from file extension
                    content_type, _ = mimetypes.guess_type(file.file.name)
            except Exception:
                pass

            # Default content type if we can't determine it
            if not content_type:
                content_type = "application/octet-stream"

            files_data.append(
                {
                    "id": file.id,
                    "url": file.file.url,
                    "name": file.file.name,
                    "size": file.file.size if hasattr(file.file, "size") else 0,
                    "type": content_type,
                }
            )

        context["file_urls"] = files_data
        return context

    @transaction.atomic
    def form_valid(self, form):
        """Procesa el formulario válido actualizando el reporte y gestionando archivos."""
        self.object = form.save()

        # Handle deletions of existing files based on kept_files (JSON array of IDs)
        existing_ids = set(self.object.files.values_list("id", flat=True))
        kept_raw = self.request.POST.get("kept_files")
        try:
            kept_ids = set(int(x) for x in json.loads(kept_raw)) if kept_raw else set(existing_ids)
        except Exception:
            # If parsing fails, assume keep all existing
            kept_ids = set(existing_ids)
        to_delete = existing_ids - kept_ids
        if to_delete:
            SimpleReportFile.objects.filter(report=self.object, id__in=to_delete).delete()

        # Save new uploaded files (MultiFileField returns list of InMemoryUploadedFile)
        new_files = form.cleaned_data.get("files") or []
        for f in new_files:
            SimpleReportFile.objects.create(report=self.object, file=f, created_by=self.request.user)

        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)

        return HttpResponseRedirect(self.get_success_url())


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar o deshabilitar reportes simples."""

    permission_required = PERMISSION_DELETE
    model = SimpleReport
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True
