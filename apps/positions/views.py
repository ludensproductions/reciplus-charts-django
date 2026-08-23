from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from apps.comun.consts import SUCCESS_GROUPS_ASSIGNED
from apps.comun.views import (
    GenericFilterView,
    GenericUpdateView,
)
from apps.positions.models import Puesto, PuestoDepartamento

from .consts import (
    DASHBOARD_URL,
    EDIT_TITLE,
    EDIT_URL,
    ERROR_POSITION_EXISTS_IN_DEPARTMENT,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    ORDERING,
    PERMISSION_ADD_GROUP,
    PERMISSION_CHANGE,
    PERMISSION_VIEW,
    PERMISSIONS_TITLE,
    PERMISSIONS_URL,
)
from .filters import PuestoFilter
from .forms import (
    PositionGroupForm,
    PuestoForm,
)
from .models import PositionGroup


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Index view to list positions by department."""

    permission_required = PERMISSION_VIEW
    model = PuestoDepartamento
    filterset_class = PuestoFilter
    template_name = "positions/index.html"

    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = ORDERING

    edit_url = EDIT_URL
    return_url = DASHBOARD_URL
    permissions_url = PERMISSIONS_URL

    def get_context_data(self, **kwargs):
        """Build the template context.

        Args:
            **kwargs: Extra context arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context["permissions_url"] = self.permissions_url
        return context


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Edit view for an existing position in a department."""

    permission_required = PERMISSION_CHANGE
    model = PuestoDepartamento
    form_class = PuestoForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def form_valid(self, form):
        """Validate and process the position edit form.

        Args:
            form (forms.Form): Validated form instance.

        Returns:
            HttpResponse: Redirect to the success URL.
        """
        # Set additional fields not in the form
        position_departament = self.get_object()

        old_position = position_departament.puesto.puesto
        new_position = form.cleaned_data.get("puesto").strip()

        departamento = position_departament.departamento

        if Puesto.objects.filter(
            puesto=new_position,
            puesto_departamento__departamento=departamento,
            puesto_departamento__deleted__isnull=True,
        ).exists():
            form.add_error("puesto", ERROR_POSITION_EXISTS_IN_DEPARTMENT)
            return self.form_invalid(form)

        if old_position != new_position:
            new_position_obj = Puesto.objects.create(puesto=new_position, created_by=self.request.user)
            position_departament.puesto = new_position_obj
            position_departament.updated_by = self.request.user
            position_departament.save()

        return HttpResponseRedirect(self.get_success_url())


class AsignarGruposView(PermissionRequiredMixin, FormView):
    """View to assign authorization groups to a position."""

    permission_required = PERMISSION_ADD_GROUP
    template_name = "generic/form.html"
    form_class = PositionGroupForm
    return_url = INDEX_URL
    title = PERMISSIONS_TITLE

    def dispatch(self, request, *args, **kwargs):
        """Load position-department relationship before handling the request.

        Args:
            request (HttpRequest): Incoming request.
            *args: Positional arguments.
            **kwargs: Keyword arguments, must include `pk`.

        Returns:
            HttpResponse: Response from the parent dispatcher.
        """
        self.puesto_departamento = get_object_or_404(PuestoDepartamento, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Add `puesto_departamento` to form kwargs.

        Returns:
            dict: Form keyword arguments.
        """
        kwargs = super().get_form_kwargs()
        kwargs["puesto_departamento"] = self.puesto_departamento
        return kwargs

    def get_initial(self):
        """Load currently assigned groups as initial values.

        Returns:
            dict: Initial form values.
        """
        current_groups = PositionGroup.objects.filter(puesto_departamento=self.puesto_departamento).values_list(
            "auth_group", flat=True
        )

        return {"grupos": list(current_groups)}

    def form_valid(self, form):
        """Persist group assignments and redirect with success message.

        Args:
            form (forms.Form): Validated form instance.

        Returns:
            HttpResponse: Redirect response.
        """
        form.save()
        messages.success(self.request, SUCCESS_GROUPS_ASSIGNED)
        return redirect(INDEX_URL)

    def get_context_data(self, **kwargs):
        """Add return_url and title to context.

        Args:
            **kwargs: Extra context arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context["return_url"] = self.return_url
        context["title"] = self.title
        return context
