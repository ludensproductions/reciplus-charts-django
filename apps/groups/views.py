from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.html import format_html, mark_safe
from django.utils.text import format_lazy

from apps.comun.consts import ERROR_ACTION_BLOCKED, ERROR_RESTORE_BLOCKED_WITH_REASON
from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericFilterView,
    GenericUpdateView,
)

from .consts import (
    ACTION_DELETE_LABEL,
    ACTION_DELETED_LABEL,
    ACTION_RESTORE_LABEL,
    ACTION_RESTORED_LABEL,
    CREATE_TITLE,
    CREATE_URL,
    DELETE_TITLE,
    DELETE_URL,
    EDIT_TITLE,
    EDIT_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    LIST_CONJUNCTION_AND,
    ORDERING,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    USERS_CATALOG_URL,
)
from .filters import GroupFilter
from .forms import GroupForm
from .models import CustomGroup


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List and filter groups."""

    permission_required = PERMISSION_VIEW
    model = CustomGroup
    filterset_class = GroupFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = ORDERING
    can_disable = True

    create_url = CREATE_URL
    delete_url = DELETE_URL
    edit_url = EDIT_URL

    return_url = USERS_CATALOG_URL


class GroupViewFormMixin:
    """Mixin for group form views with permission handling."""

    def get_context_data(self, **kwargs):
        """Build context with all permissions and current selections.

        Returns:
            dict: Template context with permission lists.
        """
        context = super().get_context_data(**kwargs)
        context["permissions"] = self.get_all_permissions()
        context["current_permissions"] = self.get_current_permissions()
        return context

    def get_current_permissions(self):
        """Return permissions currently selected for the group."""
        permission_id_list = self.request.POST.getlist("permissions")
        pk = self.kwargs.get("pk")

        if len(permission_id_list) == 0:
            if pk:
                permissions = Permission.objects.filter(group__pk=pk)
            else:
                permissions = Permission.objects.none()
        else:
            permissions = Permission.objects.filter(pk__in=permission_id_list)

        return permissions

    def get_all_permissions(self):
        """Return all available permissions excluding current selections."""
        permission_id_list = self.request.POST.getlist("permissions")

        exclude = Q(content_type__model__in=["logentry", "permission", "group"])
        exclude |= Q(content_type__app_label__in=["django_q", "contenttypes", "sessions"])
        exclude |= Q(content_type__model__startswith="historical")

        # If form errors occur, collect permissions that were not selected.
        if permission_id_list:
            exclude |= Q(pk__in=permission_id_list)
        else:
            pk = self.kwargs.get("pk")

            if pk:
                exclude |= Q(group__pk=pk)

        permissions = Permission.objects.all().exclude(exclude).order_by("content_type__model", "codename")

        return permissions


class CreateView(PermissionRequiredMixin, GroupViewFormMixin, GenericCreateView):
    """Create a new group."""

    permission_required = PERMISSION_ADD
    template_name = "groups/create.html"
    model = CustomGroup
    form_class = GroupForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, GroupViewFormMixin, GenericUpdateView):
    """Edit an existing group."""

    permission_required = PERMISSION_CHANGE
    template_name = "groups/create.html"
    model = CustomGroup
    form_class = GroupForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete a group."""

    permission_required = PERMISSION_DELETE
    model = CustomGroup
    success_url = reverse_lazy(INDEX_URL)
    title = DELETE_TITLE
    return_url = INDEX_URL
    can_disable = True

    def handle_response(self, success, message):
        """Handle responses after delete or restore attempts."""
        success_url = self.get_success_url()

        if not success:
            # Handle string messages (typically from restore operations)
            if isinstance(message, str):
                final_message = format_html(
                    ERROR_RESTORE_BLOCKED_WITH_REASON,
                    object=self.object,
                    reason=message,
                )
                messages.error(self.request, final_message)
            # Handle dictionary messages (typically from delete operations)
            else:
                blocking_info = message.get("blocking_info", [])
                all_blocking_elements = []

                # Build links to related objects
                for info in blocking_info:
                    if not info["elements"]:
                        continue

                    app_label = info["app_label"]
                    elements = info["elements"]
                    model_str = info["model_str"]
                    elements_ids = [element.id for element in elements]
                    params = f"id={','.join(map(str, elements_ids))}"

                    url_name = info.get("url_name", f"{app_label}:index")
                    try:
                        from django.urls import reverse

                        list_url = reverse(url_name)
                        list_url = f"{list_url}?{params}"
                    except Exception:
                        list_url = "#"

                    link_html = format_html("<a href='{}'>{}</a>", list_url, model_str)
                    all_blocking_elements.append(link_html)

                # Format links for display.
                if len(all_blocking_elements) > 1:
                    final_str = (
                        ", ".join(all_blocking_elements[:-1])
                        + " "
                        + LIST_CONJUNCTION_AND
                        + " "
                        + all_blocking_elements[-1]
                    )
                else:
                    final_str = ", ".join(all_blocking_elements)

                # Create appropriate message based on operation type.
                delete = message.get("delete")
                operation_type = ACTION_DELETE_LABEL if delete else ACTION_RESTORE_LABEL

                final_message = format_html(
                    ERROR_ACTION_BLOCKED,
                    action=operation_type,
                    object=self.object,
                    related=mark_safe(final_str),
                )

                messages.error(self.request, final_message)

            return self.get_response("ERROR", success_url)

        success_message = self.get_success_message()
        if success_message:
            action = ACTION_DELETED_LABEL if self.is_delete else ACTION_RESTORED_LABEL
            success_message = format_lazy(success_message, action=action)
            messages.success(self.request, success_message)

        return self.get_response("OK", success_url)

    def get_response(self, htmx_message, redirect_url):
        """Return the appropriate HTTP response for HTMX requests."""
        if self.is_htmx:
            return HttpResponse(htmx_message)
        return HttpResponseRedirect(redirect_url)
