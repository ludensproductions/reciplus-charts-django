import os
from typing import Any

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.forms import all_valid
from django.http import FileResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View

from apps.comun.formset_utils import get_records_formset_by_prefix
from apps.comun.views import (
    GenericCreateFormsetView,
    GenericDeleteView,
    GenericEditFormsetView,
    GenericFilterView,
    GenericMultiEntityDetailView,
)

from .consts import (
    ACTIVITIES_FORMSET_TITLE,
    ATTENDEES_FORMSET_TITLE,
    ATTENDEES_PREFIX,
    ATTENDEES_TITLE,
    CHILDREN_ENTITIES,
    CLONE_TITLE,
    COLOR_DANGER,
    COLOR_INFO,
    COLOR_PRIMARY,
    CREATE_TITLE,
    CREATE_URL,
    CUSTOM_BUTTON_TITLE,
    DASHBOARD_URL,
    DELETE_TITLE,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    EVENT_ACTIVITY_FORMSET_CONFIG,
    EVENT_CLONE_EVENT_URL,
    EVENT_DOWNLOAD_MAP_URL,
    EVENT_REGISTER_TO_EVENT_URL,
    FIELD_PK,
    FORM_ID,
    FORMSET_KEY_ACTIVITIES,
    ICON_CLONE_EVENT,
    ICON_DOWNLOAD_MAP,
    ICON_REGISTER_ATTENDEES,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    PDF_FILENAME,
    PDF_STATIC_PATH,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    TABLE_TITLES,
    TOOLTIP_CLONE_EVENT,
    TOOLTIP_DOWNLOAD_MAP,
    TOOLTIP_REGISTER_ATTENDEES,
    VIEW_TYPE_CLONE,
)
from .filters import EventFilter
from .forms import (
    EventActivityBaseFormSet,
    EventActivityBaseInlineFormSet,
    EventActivityForm,
    EventAddAttendeeForm,
    EventAttendeeForm,
    EventCloneActivityBaseInlineFormSet,
    EventForm,
)
from .models import Event, EventActivity, EventAttendee


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List events with filtering and extra actions."""

    permission_required = PERMISSION_VIEW
    model = Event
    filterset_class = EventFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    create_url = CREATE_URL
    edit_url = EDIT_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    return_url = DASHBOARD_URL
    can_disable = False

    register_to_event_url = EVENT_REGISTER_TO_EVENT_URL
    download_map = EVENT_DOWNLOAD_MAP_URL
    clone_event_url = EVENT_CLONE_EVENT_URL

    def get_extra_actions(self):
        """Build extra actions for each event.

        Returns:
            list[dict[str, Any]]: Action definitions for the list view.
        """
        return [
            {
                "url": self.register_to_event_url,
                "params": {FIELD_PK: FIELD_PK},
                "icon": ICON_REGISTER_ATTENDEES,
                "color": COLOR_INFO,
                "tooltip": TOOLTIP_REGISTER_ATTENDEES,
            },
            {
                "url": self.download_map,
                "icon": ICON_DOWNLOAD_MAP,
                "color": COLOR_DANGER,
                "tooltip": TOOLTIP_DOWNLOAD_MAP,
            },
            {
                "url": self.clone_event_url,
                "params": {FIELD_PK: FIELD_PK},
                "icon": ICON_CLONE_EVENT,
                "color": COLOR_PRIMARY,
                "tooltip": TOOLTIP_CLONE_EVENT,
            },
        ]


class CreateView(PermissionRequiredMixin, GenericCreateFormsetView):
    """Create a new event with activity formsets."""

    permission_required = PERMISSION_ADD
    model = Event
    form_class = EventForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formset_config = [
            {
                **EVENT_ACTIVITY_FORMSET_CONFIG,
                "form": EventActivityForm,
                "base_formset": EventActivityBaseFormSet,
                "extra": 0,
            },
        ]
        self.create_formset_classes()

    def pre_save(self, form):
        """Assign the creator user before saving.

        Args:
            form (forms.Form): Validated event form.

        Returns:
            Event: Prepared event instance.
        """
        main_instance = super().pre_save(form)
        main_instance.created_by = self.request.user
        return main_instance

    def post_save(self, main_instance, instances: dict):
        """Save related activities after the event is saved.

        Args:
            main_instance (Event): Saved event instance.
            instances (dict): Mapping of formset keys to instances.

        Returns:
            Event: Updated event instance.
        """
        activity_instances = instances[FORMSET_KEY_ACTIVITIES]
        for activity in activity_instances:
            activity.save()
        return main_instance

    def get_context_data(self, **kwargs):
        """Add custom data to the context.

        Returns:
            dict[str, Any]: Template context.
        """
        context = super().get_context_data(**kwargs)
        context["custom_button_title"] = CUSTOM_BUTTON_TITLE
        return context


class EditView(PermissionRequiredMixin, GenericEditFormsetView):
    """Edit an existing event and its activities."""

    permission_required = PERMISSION_CHANGE
    model = Event
    form_class = EventForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formset_config = [
            {
                **EVENT_ACTIVITY_FORMSET_CONFIG,
                "parent": Event,
                "child": EventActivity,
                "form": EventActivityForm,
                "inline_formset": EventActivityBaseInlineFormSet,
                # "oneToNFormsets":True,
            },
        ]
        self.create_formset_classes()

    def get_context_data(self, **kwargs):
        """Add custom data to the context.

        Returns:
            dict[str, Any]: Template context.
        """
        context = super().get_context_data(**kwargs)
        # Provide the label for the formset row removal button.
        context["custom_button_title"] = CUSTOM_BUTTON_TITLE
        context["form_id"] = FORM_ID
        return context


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete an event."""

    permission_required = PERMISSION_DELETE
    model = Event
    success_url = reverse_lazy(INDEX_URL)
    title = DELETE_TITLE
    return_url = INDEX_URL


class DetailView(PermissionRequiredMixin, GenericMultiEntityDetailView):
    """Display event details and related entities."""

    permission_required = PERMISSION_VIEW
    model = Event
    title = DETAIL_TITLE
    return_url = INDEX_URL

    shown_fields = DETAIL_FIELDS
    children_entities = CHILDREN_ENTITIES
    table_title = TABLE_TITLES


class AddEventAttendeeView(PermissionRequiredMixin, GenericEditFormsetView):
    """Add attendees to an event."""

    permission_required = PERMISSION_CHANGE
    model = Event
    form_class = EventAddAttendeeForm
    success_url = reverse_lazy(INDEX_URL)
    title = ATTENDEES_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formset_config = [
            {
                "parent": Event,
                "child": EventAttendee,
                "title": ATTENDEES_FORMSET_TITLE,
                "form": EventAttendeeForm,
                "prefix": ATTENDEES_PREFIX,
                "related_name": "event",
                # "inline_formset": EventActivityBaseInlineFormSet,
                "oneToNFormsets": True,
            },
        ]
        self.create_formset_classes()

    def get_context_data(self, **kwargs):
        """Add custom data to the context.

        Returns:
            dict[str, Any]: Template context.
        """
        context = super().get_context_data(**kwargs)
        # Provide the label for the formset row removal button.
        context["custom_button_title"] = CUSTOM_BUTTON_TITLE
        context["form_id"] = FORM_ID

        formsets = context.get("formsets", [])
        for formset_objects in formsets:
            formset = formset_objects[1]
            if not formset.prefix == ATTENDEES_PREFIX:
                continue

            if formset.queryset.count() == 0:
                formset.extra = 1

        return context


class DownloadStaticPDFView(View):
    """Download the static PDF map file."""

    def get(self, request, *args, **kwargs):
        """Handle GET requests for downloading the file.

        Returns:
            FileResponse: Streamed PDF response.
        """
        file_path = os.path.join(settings.BASE_DIR, PDF_STATIC_PATH)

        # Use FileResponse for efficient streaming of large files.
        response = FileResponse(open(file_path, "rb"), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{PDF_FILENAME}"'
        return response


class CloneEventView(PermissionRequiredMixin, GenericEditFormsetView):
    """Clone an existing event with related activities and attendees."""

    permission_required = PERMISSION_CHANGE
    model = Event
    form_class = EventForm
    success_url = reverse_lazy(INDEX_URL)
    title = CLONE_TITLE
    return_url = INDEX_URL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formset_config = [
            {
                "parent": Event,
                "child": EventActivity,
                "title": ACTIVITIES_FORMSET_TITLE,
                "form": EventActivityForm,
                "prefix": FORMSET_KEY_ACTIVITIES,
                "related_name": "event",
                "inline_formset": EventCloneActivityBaseInlineFormSet,
                # "oneToNFormsets":True,
            },
        ]
        self.create_formset_classes()

    def get_context_data(self, **kwargs):
        """Add custom data to the context.

        Returns:
            dict[str, Any]: Template context.
        """
        context = super().get_context_data(**kwargs)
        # Provide the label for the formset row removal button.
        context["custom_button_title"] = CUSTOM_BUTTON_TITLE
        context["form_id"] = FORM_ID
        return context

    def get_form_kwargs(self):
        """Add additional keyword arguments for the form.

        Returns:
            dict[str, Any]: Form keyword arguments.
        """
        kwargs = super().get_form_kwargs()
        kwargs["view_type"] = VIEW_TYPE_CLONE
        return kwargs

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Handle POST requests to clone the event.

        Returns:
            HttpResponse: Redirect response on success or a rendered form.
        """
        self.object = self.get_object()
        user = request.user
        form = self.form_class(request.POST, instance=self.object, user=user)
        formsets = [
            formset_config.get("formset_class")(request.POST, **self.get_formset_kwargs(formset_config))
            for formset_config in self.get_formset_config()
        ]

        if form.is_valid() and all_valid(formsets):
            main_instance = self.pre_save(form)
            main_instance.save()
            form.save_m2m()
            new_child_instances = {}
            edited_child_instances = {}

            for formset_config, formset in zip(self.get_formset_config(), formsets):
                child_instances = []
                new_instances = []
                ids_inside_post = get_records_formset_by_prefix(request, formset.prefix)

                formset_config.get("child").objects.filter(
                    **{formset_config.get("related_name"): main_instance}
                ).exclude(id__in=ids_inside_post).delete()

                for child_form in formset:
                    child_form_instance = child_form.save(commit=False)
                    child_form_instance.pk = None
                    setattr(child_form_instance, formset_config.get("related_name"), main_instance)

                    child_form_instance = self.process_formset_instance(
                        child_form_instance, formset_config, main_instance
                    )

                    if child_form_instance.pk:
                        child_instances.append(child_form_instance)
                        continue

                    new_instances.append(child_form_instance)

                new_objs, child_instances = self.save_formset(formset_config, new_instances, child_instances)
                new_child_instances.update({formset_config.get("prefix"): new_objs})
                edited_child_instances.update({formset_config.get("prefix"): child_instances})

                attendees = list(EventAttendee.objects.filter(event_id=self.kwargs.get("pk"), deleted__isnull=True))

                for attendee in attendees:
                    attendee.pk = None
                    attendee.event = main_instance
                    attendee.save()

            main_instance = self.post_save(main_instance, new_child_instances, edited_child_instances)

            if self.get_success_message(cleaned_data=form.cleaned_data):
                messages.success(self.request, self.get_success_message(form.cleaned_data))
            return redirect(self.get_success_url())

        context = self.get_context_data()
        context["form"] = form
        context["formsets"] = [
            (formset_config, formset_instance)
            for formset_config, formset_instance in zip(self.get_formset_config(), formsets)
        ]
        return self.render_to_response(context)

    def pre_save(self, form: forms.Form) -> Any:
        """Prepare the instance before saving.

        Args:
            form (forms.Form): Validated event form.

        Returns:
            Any: Unsaved event instance with creator assigned.
        """
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.pk = None
        return instance
