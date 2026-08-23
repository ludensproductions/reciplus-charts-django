from crispy_forms.helper import FormHelper
from django import forms
from django.forms import ModelChoiceField
from django.utils.text import format_lazy

from apps.comun.consts import RegexValidator
from apps.comun.forms import AbstractModelForm, GenericBaseFormSet, GenericBaseInlineFormSet
from apps.comun.select2.widgets import GenericSelect2Widget
from apps.users.models import User
from utils.sequences import get_sequence

from . import consts as event_planner_consts
from .consts import VIEW_TYPE_CLONE
from .models import Event, EventActivity, EventAttendee


def make_responsible_field(
    model,
    field_name,
    tags="true",
    dependent_fields=None,
    disabled=False,
    required=True,
    **kwargs,
):
    """Creates a ModelChoiceField for responsible user selection with a custom widget.

    Args:
        model: The model class to use for the queryset.
        field_name: The field or fields to search by.
        tags (str, optional): Whether to allow tags. Defaults to "true".
        dependent_fields (dict, optional): Dependent fields for the widget. Defaults to None.
        disabled (bool, optional): Whether the field is disabled. Defaults to False.
        required (bool, optional): Whether the field is required. Defaults to True.
        **kwargs: Additional keyword arguments for ModelChoiceField.

    Returns:
        ModelChoiceField: The configured field.
    """
    # Build search_fields based on the field_name type.
    if isinstance(field_name, (list, tuple)):
        search_fields = [f"{f}__icontains" for f in field_name]
    else:
        search_fields = [f"{field_name}__icontains"]

    widget = GenericSelect2Widget(
        model=model,
        search_fields=search_fields,
        dependent_fields=dependent_fields or {},
        attrs={
            "data-model": model._meta.label,
            "data-tags": tags,
        },
    )

    return ModelChoiceField(
        queryset=model.objects.all(),
        widget=widget,
        disabled=disabled,
        required=required,
        **kwargs,
    )


class EventForm(AbstractModelForm):
    """Form for creating and updating Event instances."""

    responsible = make_responsible_field(
        User,
        ["first_name", "last_name"],
        tags="false",
        label=event_planner_consts.EVENT_RESPONSIBLE_LABEL,
    )

    class Meta:
        """Meta options for EventForm.

        Attributes:
            model: The model associated with the form.
            fields: List of fields to include in the form.
            exclude: List of fields to exclude from the form.
            labels: Dictionary of field labels.
            widgets: Dictionary of field widgets.
        """

        model = Event
        fields = ["title", "date_start", "location", "responsible"]
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]

        labels = {
            "title": event_planner_consts.EVENT_TITLE_LABEL,
            "date_start": event_planner_consts.EVENT_DATE_START_LABEL,
            "location": event_planner_consts.EVENT_LOCATION_LABEL,
        }

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": event_planner_consts.EVENT_TITLE_PLACEHOLDER}),
            "date_start": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "location": forms.TextInput(attrs={"placeholder": event_planner_consts.EVENT_LOCATION_PLACEHOLDER}),
            "responsible": forms.Select(attrs={"class": "input_formset"}),
        }

    def __init__(self, *args, **kwargs):
        """Initializes the EventForm, sets up labels, and handles clone view logic.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. Can include 'view_type'.
        """
        self.view_type = kwargs.pop("view_type", None)
        super().__init__(*args, **kwargs)

        self.fields["responsible"].label_from_instance = lambda obj: (
            format_lazy(
                event_planner_consts.RESPONSIBLE_DISPLAY_COMMA,
                first_name=obj.first_name,
                last_name=obj.last_name,
            )
        )

        if self.view_type == VIEW_TYPE_CLONE:
            max_len = self.fields["title"].max_length
            prefix = event_planner_consts.CLONE_TITLE_PREFIX
            original_title = self.instance.title or ""

            # Ensure the cloned title fits the field length.
            available_len = max_len - len(prefix)
            truncated_title = original_title[:available_len]

            self.initial["title"] = f"{prefix}{truncated_title}"

    def save(self, commit=True):
        """Saves the Event instance, generating a folio if needed.

        Args:
            commit (bool): Whether to save the instance to the database.

        Returns:
            Event: The saved Event instance.
        """
        instance = super().save(commit=False)
        if not instance.folio:
            instance.folio = get_sequence("event_folio_sequence")

        if commit:
            instance.save()
        return instance


class EventActivityForm(AbstractModelForm):
    """Form for creating and updating EventActivity instances."""

    class Meta:
        """Meta options for EventActivityForm.

        Attributes:
            model: The model associated with the form.
            fields: List of fields to include in the form.
            exclude: List of fields to exclude from the form.
            labels: Dictionary of field labels.
            widgets: Dictionary of field widgets.
        """

        model = EventActivity
        fields = ["activity", "capacity", "code"]
        exclude = ["is_deleted", "deleted_at", "event", "created_by", "updated_by"]

        labels = {
            "activity": event_planner_consts.EVENT_ACTIVITY_LABEL,
            "capacity": event_planner_consts.EVENT_ACTIVITY_CAPACITY_LABEL,
            "code": event_planner_consts.EVENT_ACTIVITY_CODE_LABEL,
        }

        widgets = {
            "activity": forms.Select(attrs={"class": "input_formset"}),
            "capacity": forms.NumberInput(
                attrs={
                    "placeholder": event_planner_consts.EVENT_ACTIVITY_CAPACITY_PLACEHOLDER,
                    "class": "input_formset",
                }
            ),
            "code": forms.TextInput(
                attrs={"placeholder": event_planner_consts.EVENT_ACTIVITY_CODE_PLACEHOLDER, "class": "input_formset"}
            ),
        }

    def __init__(self, *args, **kwargs):
        """Initializes the EventActivityForm and sets up labels and helpers.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.fields["activity"].required = True

        # Concatenate name and location for select labels.
        self.fields["activity"].label_from_instance = lambda obj: (
            format_lazy(
                event_planner_consts.ACTIVITY_LABEL_WITH_LOCATION,
                name=obj.name,
                location=obj.location,
            )
        )


def validate_event_activity_formset(forms, formset, is_clone=False):
    """Validates a formset of EventActivity forms for duplicates and required fields.

    Args:
        forms (list): List of EventActivity forms.
        formset: The formset instance.
        is_clone (bool, optional): Whether this is a clone operation. Defaults to False.
    """
    seen_activity_code = set()
    seen_codes = set()

    if len(forms) == 0:
        formset._non_form_errors = formset.error_class([event_planner_consts.ERROR_ACTIVITY_REQUIRED])

    for form in forms:
        if not form.cleaned_data:
            # Keep validation limited to fields that exist in the payload.
            cleaned_data = {}
        else:
            cleaned_data = form.cleaned_data

        # Stop extra validation when model validation fails to avoid multiple errors.
        if not form.is_valid():
            continue

        activity = cleaned_data.get("activity")
        code = cleaned_data.get("code")
        instance_id = getattr(form.instance, "id", None)
        code_error_added = False

        if not code:
            form.add_error("code", event_planner_consts.ERROR_FIELD_REQUIRED)

        elif not RegexValidator.validate(code, RegexValidator.ALPHANUMERIC):
            form.add_error("code", event_planner_consts.ERROR_CODE_ALPHANUMERIC)

        key = (activity.id if activity else None, code)
        if key in seen_activity_code:
            form.add_error("activity", event_planner_consts.ERROR_ACTIVITY_CODE_DUPLICATE)
        seen_activity_code.add(key)

        if code in seen_codes:
            form.add_error("code", event_planner_consts.ERROR_CODE_DUPLICATE)
            code_error_added = True
        seen_codes.add(code)

        if is_clone:
            instance_id = None

        if not code_error_added and code and EventActivity.objects.filter(code=code).exclude(id=instance_id).exists():
            form.add_error("code", event_planner_consts.ERROR_CODE_ALREADY_EXISTS)
            code_error_added = True


class EventActivityBaseFormSet(GenericBaseFormSet):
    """Base formset for EventActivity with custom clean logic."""

    def clean(self):
        """Cleans the formset and validates for duplicates and required fields."""
        super().clean()
        validate_event_activity_formset(self.forms, self)


class EventActivityBaseInlineFormSet(GenericBaseInlineFormSet):
    """Base inline formset for EventActivity with custom clean logic."""

    def clean(self):
        """Cleans the inline formset and validates for duplicates and required fields."""
        super().clean()
        validate_event_activity_formset(self.forms, self)


class EventCloneActivityBaseInlineFormSet(GenericBaseInlineFormSet):
    """Base inline formset for cloning EventActivity with custom clean logic."""

    def clean(self):
        """Cleans the inline formset and validates for duplicates and required fields (clone mode)."""
        super().clean()
        validate_event_activity_formset(self.forms, self, is_clone=True)


class EventAddAttendeeForm(AbstractModelForm):
    """Form for adding attendees to an event."""

    class Meta:
        """Meta options for EventAddAttendeeForm.

        Attributes:
            model: The model associated with the form.
            fields: List of fields to include in the form.
            exclude: List of fields to exclude from the form.
            widgets: Dictionary of field widgets.
        """

        model = Event
        fields = ["title"]
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": event_planner_consts.EVENT_TITLE_PLACEHOLDER}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].disabled = True


class EventAttendeeForm(AbstractModelForm):
    """Form for creating and updating EventAttendee instances."""

    class Meta:
        """Meta options for EventAttendeeForm.

        Attributes:
            model: The model associated with the form.
            fields: List of fields to include in the form.
            labels: Dictionary of field labels.
            widgets: Dictionary of field widgets.
        """

        model = EventAttendee
        fields = ["full_name", "email", "phone", "notes"]

        labels = {
            "full_name": event_planner_consts.ATTENDEE_FULL_NAME_LABEL,
            "email": event_planner_consts.ATTENDEE_EMAIL_LABEL,
            "phone": event_planner_consts.ATTENDEE_PHONE_LABEL,
            "notes": event_planner_consts.ATTENDEE_NOTES_LABEL,
        }

        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": event_planner_consts.ATTENDEE_FULL_NAME_PLACEHOLDER}),
            "email": forms.EmailInput(attrs={"placeholder": event_planner_consts.ATTENDEE_EMAIL_PLACEHOLDER}),
            "phone": forms.TextInput(attrs={"placeholder": event_planner_consts.ATTENDEE_PHONE_PLACEHOLDER}),
            "notes": forms.Textarea(attrs={"placeholder": event_planner_consts.ATTENDEE_NOTES_PLACEHOLDER, "rows": 3}),
        }
