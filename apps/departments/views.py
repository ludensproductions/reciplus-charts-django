from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import all_valid
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django_select2.views import AutoResponseView
from simple_history.utils import bulk_create_with_history

from apps.comun.consts import SUCCESS_GROUPS_ASSIGNED
from apps.comun.formset_utils import get_records_formset_by_prefix
from apps.comun.views import (
    GenericCreateFormsetView,
    GenericDeleteView,
    GenericEditFormsetView,
    GenericFilterView,
    GenericMultiEntityDetailView,
)
from apps.departments.models import Departamento, GruposDepartamento
from apps.positions.models import PuestoDepartamento
from apps.users.models import User

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
    DISABLED_INDEX_TITLE,
    DISABLED_URL,
    EDIT_TITLE,
    EDIT_URL,
    ENABLE_URL,
    FILTER_FIELDS,
    GROUPS_TITLE,
    GROUPS_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    ORDERING,
    PERMISSION_ADD,
    PERMISSION_ADD_GROUPS,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_ENABLE,
    PERMISSION_VIEW,
    PERMISSION_VIEW_POSITION,
    POSITION_FORMSET_CONFIG,
    TABLE_TITLES,
)
from .forms import DepartmentForm, GruposDepartamentoForm, PositionForm, PositionFormSet, PositionInlineFormSet


class PositionSelect2responseView(PermissionRequiredMixin, AutoResponseView):
    """Serve Select2 responses for positions."""

    permission_required = PERMISSION_VIEW_POSITION


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List and filter departments."""

    permission_required = PERMISSION_VIEW
    model = Departamento
    template_name = "departments/index.html"
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = ORDERING

    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    disable_url = DISABLED_URL
    return_url = DASHBOARD_URL
    groups_url = GROUPS_URL

    def get_context_data(self, **kwargs):
        """Build the view context with the groups URL.

        Returns:
            dict[str, Any]: Template context.
        """
        context = super().get_context_data(**kwargs)
        context["groups_url"] = self.groups_url
        return context


class CreateView(PermissionRequiredMixin, GenericCreateFormsetView):
    """Create new departments with position formsets."""

    permission_required = PERMISSION_ADD
    model = Departamento
    form_class = DepartmentForm
    template_name = "departments/formset.html"
    success_url = reverse_lazy(INDEX_URL)
    return_url = INDEX_URL
    title = CREATE_TITLE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formset_config = [
            {
                **POSITION_FORMSET_CONFIG,
                "form": PositionForm,
                "base_formset": PositionFormSet,
            },
        ]
        self.create_formset_classes()

    def get_context_data(self, **kwargs):
        """Build the view context with the custom button label.

        Returns:
            dict[str, Any]: Template context.
        """
        context = super().get_context_data(**kwargs)
        # Provide a custom label for formset row removal.
        context["custom_button_title"] = CUSTOM_BUTTON_TITLE
        return context


class EditView(PermissionRequiredMixin, GenericEditFormsetView):
    """Edit existing departments and their positions."""

    permission_required = PERMISSION_CHANGE
    model = Departamento
    form_class = DepartmentForm
    template_name = "departments/formset.html"
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formset_config = [
            {
                **POSITION_FORMSET_CONFIG,
                "parent": Departamento,
                "child": PuestoDepartamento,
                "form": PositionForm,
                "inline_formset": PositionInlineFormSet,
            },
        ]
        self.create_formset_classes()

    def post(self, request, *args, **kwargs):
        """Handle POST request for department update."""
        self.object = self.get_object()
        user = request.user
        form = self.form_class(request.POST, instance=self.object, user=user)
        formsets = [
            formset_config.get("formset_class")(request.POST, **self.get_formset_kwargs(formset_config))
            for formset_config in self.get_formset_config()
        ]

        form_valid = form.is_valid()
        all_formsets_valid = all_valid(formsets)

        if not form_valid or not all_formsets_valid:
            context = self.get_context_data()
            context["form"] = form
            context["formsets"] = [
                (formset_config, formset_instance)
                for formset_config, formset_instance in zip(self.get_formset_config(), formsets)
            ]
            return self.render_to_response(context)

        main_instance = self.pre_save(form)
        main_instance.save()

        new_child_instances = {}
        edited_child_instances = {}

        for formset_config, formset in zip(self.get_formset_config(), formsets):
            child_instances = []
            new_instances = []
            ids_inside_post = get_records_formset_by_prefix(request, formset.prefix)

            objects_to_delete = (
                formset_config.get("child")
                .objects.filter(**{formset_config.get("related_name"): main_instance})
                .exclude(id__in=ids_inside_post)
            )

            if formset_config.get("form").__name__ == "PositionForm":
                puestos_to_unlink_users = [puesto.puesto.id for puesto in objects_to_delete]
                User.objects.filter(puesto_id__in=puestos_to_unlink_users, departamento=main_instance).update(
                    puesto=None
                )

            objects_to_delete.delete()

            for child_form in formset:
                child_form_instance = child_form.save(commit=False)
                child_form_instance = self.process_formset_instance(child_form_instance, formset_config, main_instance)

                if not child_form_instance.pk:
                    new_instances.append(child_form_instance)
                    continue

                child_instances.append(child_form_instance)

                if formset_config.get("form").__name__ != "PositionForm":
                    continue

                initial_puesto_id = child_form.initial.get("puesto")
                current_puesto_id = getattr(child_form_instance.puesto, "pk", None)

                if not initial_puesto_id or initial_puesto_id == current_puesto_id:
                    continue

                # Update users that were assigned to the previous position.
                User.objects.filter(puesto_id=initial_puesto_id, departamento=main_instance).update(
                    puesto=child_form_instance.puesto,
                )

            new_objs, child_instances = self.save_formset(formset_config, new_instances, child_instances)
            new_child_instances.update({formset_config.get("prefix"): new_objs})
            edited_child_instances.update({formset_config.get("prefix"): child_instances})

        main_instance = self.post_save(main_instance, new_child_instances, edited_child_instances)

        if self.get_success_message(cleaned_data=form.cleaned_data):
            messages.success(self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.get_success_url())


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete or disable departments."""

    permission_required = PERMISSION_DELETE
    model = Departamento
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True

    def delete(self, request, *args, **kwargs):
        """Delete the department and update related user assignments.

        Returns:
            HttpResponse: Response from the delete handler.
        """
        self.object = self.get_object()
        deleted, message = self.object.delete()

        # PuestoDepartamento.objects.filter(departamento=self.object).delete()
        User.objects.filter(departamento=self.object).update(departamento=None)
        User.objects.filter(puesto__puesto_departamento__departamento=self.object).update(puesto=None)

        return self.handle_response(deleted, message)

    # def form_valid(self, form):
    # 	instance = self.get_object()
    # 	print("*"*100)
    # 	User.objects.filter(departamento=instance).update(departamento=None)
    # 	User.objects.filter(puesto__puesto_departamento__departamento=instance).update(puesto=None)

    # 	return super().form_valid(form)


class DetailView(PermissionRequiredMixin, GenericMultiEntityDetailView):
    """Display department details and related entities."""

    permission_required = PERMISSION_VIEW
    model = Departamento
    context_object_name = CONTEXT_OBJECT_NAME
    return_url = INDEX_URL
    title = DETAIL_TITLE

    shown_fields = DETAIL_FIELDS
    children_entities = CHILDREN_ENTITIES
    table_title = TABLE_TITLES


class DisabledIndexView(PermissionRequiredMixin, GenericFilterView):
    """List disabled departments."""

    model = Departamento
    permission_required = PERMISSION_ENABLE
    title = DISABLED_INDEX_TITLE
    ordering = ORDERING
    backward = INDEX_URL
    is_disabled_view = True
    queryset = Departamento.deleted_objects.all()

    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    delete_url = ENABLE_URL
    return_url = INDEX_URL


class EnableView(PermissionRequiredMixin, GenericDeleteView):
    """Enable a previously disabled department."""

    permission_required = PERMISSION_DELETE
    model = Departamento
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True
    is_delete = False


class AddGroupView(PermissionRequiredMixin, FormView):
    """Add groups to a department."""

    permission_required = PERMISSION_ADD_GROUPS
    form_class = GruposDepartamentoForm
    template_name = "generic/form.html"
    success_url = reverse_lazy(INDEX_URL)
    return_url = INDEX_URL
    title = GROUPS_TITLE
    success_message = SUCCESS_GROUPS_ASSIGNED

    def dispatch(self, request, *args, **kwargs):
        """Load the department before processing the request.

        Returns:
            HttpResponse: Response from the parent dispatch.
        """
        self.departamento = get_object_or_404(Departamento, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """Return the department's current groups as initial values.

        Returns:
            dict[str, list[int]]: Initial data for the form.
        """
        current_groups = GruposDepartamento.objects.filter(departamento=self.departamento).values_list(
            "auth_group", flat=True
        )
        return {"auth_group": list(current_groups)}

    def get_context_data(self, **kwargs):
        """Build the context with title and return URL.

        Returns:
            dict[str, Any]: Template context.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["return_url"] = self.return_url
        return context

    def form_valid(self, form):
        """Update department groups for a valid form.

        Args:
            form (GruposDepartamentoForm): Validated form instance.

        Returns:
            HttpResponse: Redirect response on success.
        """
        groups_objects = form.cleaned_data["auth_group"]
        new_groups_ids = set(grupo.id for grupo in groups_objects)

        current_ids = set(
            GruposDepartamento.objects.filter(departamento=self.departamento).values_list("auth_group", flat=True)
        )

        groups_ids_to_add = new_groups_ids - current_ids
        groups_ids_to_delete = current_ids - new_groups_ids

        new_objects = [grupo for grupo in groups_objects if grupo.id in groups_ids_to_add]
        bulk_create_with_history(
            [GruposDepartamento(auth_group=grupo, departamento=self.departamento) for grupo in new_objects],
            model=GruposDepartamento,
        )

        if groups_ids_to_delete:
            GruposDepartamento.objects.filter(
                departamento=self.departamento, auth_group__in=groups_ids_to_delete
            ).delete()

        messages.success(self.request, self.success_message)
        return super().form_valid(form)
