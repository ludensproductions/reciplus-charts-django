import operator
import re
from functools import reduce

from django import forms
from django.db.models import Q
from django.forms import ModelChoiceField
from django.utils.text import format_lazy

from apps.comun.consts import (
    ERROR_MAX_LENGTH,
    ERROR_MAX_VALUE,
    ERROR_MIN_VALUE,
    ERROR_NEGATIVE_NUMBER,
    ERROR_REQUIRED_FIELD,
)
from apps.comun.forms import AbstractModelForm
from apps.comun.select2.widgets import GenericSelect2Widget
from apps.movies.models import Movie

from .consts import (
    ERROR_BILLING_FILE_EXTENSION,
    ERROR_BILLING_FILE_REQUIRED,
    ERROR_MODIFICATION_DATE_BEFORE_REGISTRATION,
    ERROR_MOVIE_COVER_EXTENSION,
    ERROR_MOVIE_COVER_REQUIRED,
    ERROR_PASSWORD_COMPLEXITY,
    ERROR_PHONE_INVALID_LENGTH,
    ERROR_REGISTRATION_DATE_REQUIRED_BEFORE_MODIFICATION,
    FIELD_BILLING_FILE_LABEL,
    FIELD_EMAIL_LABEL,
    FIELD_MODIFICATION_DATE_LABEL,
    FIELD_MOVIE_COVER_LABEL,
    FIELD_MOVIE_LABEL,
    FIELD_PASSWORD_LABEL,
    FIELD_PHONE_LABEL,
    FIELD_PRODUCTOR_LABEL,
    FIELD_QUANTITY_LABEL,
    FIELD_REGISTRATION_DATE_LABEL,
    FORM_CURP_LABEL,
    FORM_CURP_PLACEHOLDER,
    FORM_JUSTIFICATION_LABEL,
    FORM_JUSTIFICATION_PLACEHOLDER,
    FORM_MOVIE_LABEL_FORMAT,
    FORM_RFC_LABEL,
    FORM_RFC_PLACEHOLDER,
)
from .models import MovieInventory


class TruncatedMovieSelect2Widget(GenericSelect2Widget):
    """Select2 widget that truncates labels and supports split-term searches."""

    def __init__(self, *args, max_length=50, truncate_suffix="...", label_format=None, **kwargs):
        """Initialize the widget.

        Args:
            *args: Positional arguments.
            max_length (int): Max length before truncation.
            truncate_suffix (str): Suffix to append when truncating.
            label_format (callable | None): Optional formatter for labels.
            **kwargs: Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.max_length = max_length
        self.truncate_suffix = truncate_suffix
        self.label_format = label_format

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        """Filter with support for split terms using separators.

        Args:
            request (HttpRequest): Incoming request.
            term (str | None): Search term.
            queryset (QuerySet | None): Optional base queryset.
            **dependent_fields: Extra dependent filters.

        Returns:
            QuerySet: Filtered queryset.
        """
        if queryset is None:
            queryset = self.get_queryset()

        # Split terms when the custom separator is present.
        if term and " - " in term:
            parts = [part.strip() for part in term.split(" - ")]

            queries = []
            for part in parts:
                part_queries = [Q(**{field: part}) for field in self.search_fields]
                if part_queries:
                    queries.append(reduce(operator.or_, part_queries))

            if queries:
                combined_query = reduce(operator.or_, queries)
                queryset = queryset.filter(combined_query)

                if dependent_fields:
                    queryset = queryset.filter(**dependent_fields)

                return queryset.distinct()

        # Use parent behavior when no separator is present.
        return super().filter_queryset(request, term, queryset, **dependent_fields)

    def truncate_text(self, text):
        """Truncate text using a separator-aware strategy.

        Args:
            text (str | None): Text to truncate.

        Returns:
            str | None: Truncated text.
        """
        if not text or not self.max_length:
            return text

        separators = [" - ", ", ", "; ", " / ", " | "]

        detected_separator = None
        for sep in separators:
            if sep in text:
                detected_separator = sep
                break

        if detected_separator:
            parts = text.split(detected_separator)
            truncated_parts = []

            for part in parts:
                if len(part) > self.max_length:
                    truncated_parts.append(part[: self.max_length] + self.truncate_suffix)
                else:
                    truncated_parts.append(part)

            return detected_separator.join(truncated_parts)

        if len(text) <= self.max_length:
            return text

        return text[: self.max_length] + self.truncate_suffix

    def label_from_instance(self, obj):
        """Build a formatted and truncated label from a model instance.

        Args:
            obj (Any): Model instance.

        Returns:
            str: Label to display.
        """
        if self.label_format:
            label = self.label_format(obj)
        else:
            label = super().label_from_instance(obj)

        return self.truncate_text(str(label))


def make_movie_field(
    model,
    field_name,
    tags="true",
    dependent_fields=None,
    disabled=False,
    required=True,
    max_length=50,
    label_format=None,
    **kwargs,
):
    """Create a Movie-select field with a Select2 widget.

    Args:
        model (type[Model]): Model class for the queryset.
        field_name (str | list[str] | tuple[str, ...]): Field(s) to search.
        tags (str): Select2 tags flag.
        dependent_fields (dict | None): Dependent field mapping.
        disabled (bool): Disable the field.
        required (bool): Mark the field as required.
        max_length (int): Max label length before truncation.
        label_format (callable | None): Optional label formatter.
        **kwargs: Extra ModelChoiceField kwargs.

    Returns:
        ModelChoiceField: Configured model choice field.
    """
    # Build search_fields according to the field_name type.
    if isinstance(field_name, (list, tuple)):
        search_fields = [f"{f}__icontains" for f in field_name]
    else:
        search_fields = [f"{field_name}__icontains"]

    widget = TruncatedMovieSelect2Widget(
        model=model,
        search_fields=search_fields,
        dependent_fields=dependent_fields or {},
        max_length=max_length,
        label_format=label_format,
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


class MovieInventoryForm(AbstractModelForm):
    """Form for managing movie inventory records."""

    movie = make_movie_field(
        Movie,
        ["title", "year"],
        tags="false",
        label=FIELD_MOVIE_LABEL,
        max_length=50,
        label_format=lambda obj: format_lazy(FORM_MOVIE_LABEL_FORMAT, year=obj.year, title=obj.title),
    )

    class Meta:
        model = MovieInventory
        fields = [
            "movie",
            "productor",
            "quantity",
            "email",
            "password",
            "registration_date",
            "modification_date",
            "phone",
            "curp",
            "rfc",
            "billing_file",
            "movie_cover",
        ]

        labels = {
            "movie": FIELD_MOVIE_LABEL,
            "productor": FIELD_PRODUCTOR_LABEL,
            "quantity": FIELD_QUANTITY_LABEL,
            "email": FIELD_EMAIL_LABEL,
            "password": FIELD_PASSWORD_LABEL,
            "registration_date": FIELD_REGISTRATION_DATE_LABEL,
            "modification_date": FIELD_MODIFICATION_DATE_LABEL,
            "phone": FIELD_PHONE_LABEL,
            "billing_file": FIELD_BILLING_FILE_LABEL,
            "movie_cover": FIELD_MOVIE_COVER_LABEL,
            "curp": FORM_CURP_LABEL,
            "rfc": FORM_RFC_LABEL,
        }

        widgets = {
            "productor": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "registration_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "min": "2024-01-01"},
                format="%Y-%m-%d",
            ),
            "modification_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "max": "2026-12-31"},
                format="%Y-%m-%d",
            ),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "curp": forms.TextInput(attrs={"class": "form-control", "placeholder": FORM_CURP_PLACEHOLDER}),
            "rfc": forms.TextInput(attrs={"class": "form-control", "placeholder": FORM_RFC_PLACEHOLDER}),
            "billing_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "movie_cover": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form and set edit-mode defaults."""
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["movie"].widget.attrs["disabled"] = True
            self.fields["movie"].required = False
            self.fields["password"].required = False
            self.fields["registration_date"].initial = format(self.instance.registration_date, "Y-m-d")
            if self.instance.modification_date:
                self.fields["modification_date"].initial = format(self.instance.modification_date, "Y-m-d")

    def clean_movie(self):
        """Validate movie selection and preserve existing value on edit.

        Returns:
            Movie: Selected movie instance.

        Raises:
            ValidationError: When movie is missing on create.
        """
        movie = self.cleaned_data.get("movie")

        # Keep current movie on edit mode.
        if self.instance and self.instance.pk:
            return self.instance.movie

        # Require movie during creation.
        if not movie:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)

        return movie

    def clean_productor(self):
        """Validate producer field length and presence.

        Returns:
            str: Validated producer value.

        Raises:
            ValidationError: When value is missing or too long.
        """
        productor = self.cleaned_data.get("productor")
        if not productor:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)
        if len(productor) > 255:
            raise forms.ValidationError(format_lazy(ERROR_MAX_LENGTH, max_length=255))
        return productor

    def clean_quantity(self):
        """Validate quantity bounds.

        Returns:
            int: Validated quantity.

        Raises:
            ValidationError: When quantity is missing or out of range.
        """
        quantity = self.cleaned_data.get("quantity")
        if not quantity:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)
        if quantity < 0:
            raise forms.ValidationError(ERROR_NEGATIVE_NUMBER)
        elif quantity < 2:
            raise forms.ValidationError(format_lazy(ERROR_MIN_VALUE, min_value=2))
        elif quantity > 99999:
            raise forms.ValidationError(format_lazy(ERROR_MAX_VALUE, max_value=99999))
        return quantity

    def clean_email(self):
        """Validate email presence and max length.

        Returns:
            str: Validated email.

        Raises:
            ValidationError: When email is missing or too long.
        """
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)
        if len(email) > 255:
            raise forms.ValidationError(format_lazy(ERROR_MAX_LENGTH, max_length=255))

        return email

    def clean_password(self):
        """Validate password presence, length, and complexity.

        Returns:
            str: Validated password.

        Raises:
            ValidationError: When password is missing or invalid.
        """
        password = self.cleaned_data.get("password")
        if not password and self.instance.pk:
            return self.instance.password
        if not password:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)
        if len(password) > 20:
            raise forms.ValidationError(format_lazy(ERROR_MAX_LENGTH, max_length=20))
        if not self.validate_password_complexity(password):
            raise forms.ValidationError(ERROR_PASSWORD_COMPLEXITY)
        return password

    def clean_registration_date(self):
        """Validate registration date presence.

        Returns:
            date: Registration date.

        Raises:
            ValidationError: When date is missing.
        """
        registration_date = self.cleaned_data.get("registration_date")
        if not registration_date:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)
        return registration_date

    def clean_modification_date(self):
        """Validate modification date ordering.

        Returns:
            date | None: Modification date.

        Raises:
            ValidationError: When modification date is inconsistent.
        """
        modification_date = self.cleaned_data.get("modification_date")
        registration_date = self.cleaned_data.get("registration_date")
        if modification_date and not registration_date:
            raise forms.ValidationError(ERROR_REGISTRATION_DATE_REQUIRED_BEFORE_MODIFICATION)
        if modification_date and registration_date and modification_date < registration_date:
            raise forms.ValidationError(ERROR_MODIFICATION_DATE_BEFORE_REGISTRATION)

        return modification_date

    def clean_phone(self):
        """Validate phone number length and format.

        Returns:
            str: Validated phone value.

        Raises:
            ValidationError: When phone is missing or invalid.
        """
        phone = self.cleaned_data.get("phone")
        if not phone:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)
        if len(phone) > 15:
            raise forms.ValidationError(format_lazy(ERROR_MAX_LENGTH, max_length=15))
        if self.validate_phone_number(phone):
            raise forms.ValidationError(ERROR_PHONE_INVALID_LENGTH)
        return phone

    def clean_billing_file(self):
        """Validate billing file presence and extension.

        Returns:
            UploadedFile: Billing file.

        Raises:
            ValidationError: When file is missing or extension is invalid.
        """
        billing_file = self.cleaned_data.get("billing_file")
        if not billing_file:
            raise forms.ValidationError(ERROR_BILLING_FILE_REQUIRED)

        if billing_file.name.split(".")[-1] not in ["pdf", "zip"]:
            raise forms.ValidationError(ERROR_BILLING_FILE_EXTENSION)
        return billing_file

    def clean_movie_cover(self):
        """Validate movie cover presence and extension.

        Returns:
            UploadedFile: Movie cover file.

        Raises:
            ValidationError: When file is missing or extension is invalid.
        """
        movie_cover = self.cleaned_data.get("movie_cover")
        if not movie_cover:
            raise forms.ValidationError(ERROR_MOVIE_COVER_REQUIRED)

        if movie_cover.name.split(".")[-1] not in ["png", "jpg"]:
            raise forms.ValidationError(ERROR_MOVIE_COVER_EXTENSION)
        return movie_cover

    def validate_password_complexity(self, password):
        """Check password complexity requirements.

        Args:
            password (str): Password value.

        Returns:
            bool: True when password matches the complexity pattern.
        """
        # Combined pattern enforcing all complexity requirements.
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).{10,}$"

        return bool(re.search(pattern, password))

    def validate_phone_number(self, value):
        """Validate phone number format.

        Args:
            value (str): Phone value.

        Returns:
            bool: True when the phone number is invalid.
        """
        pattern = r"^[0-9]{10,}$"
        return not re.match(pattern, value)


class EnableMovieInventaryForm(AbstractModelForm):
    """Form for enabling a movie inventory record with justification."""

    def clean_justification(self):
        """Validate justification presence.

        Returns:
            str: Justification text.

        Raises:
            ValidationError: When justification is missing.
        """
        justification = self.cleaned_data.get("justification")
        if not justification:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)
        return justification

    class Meta:
        model = MovieInventory
        fields = ["justification"]
        exclude = [
            "movie",
            "productor",
            "quantity",
            "email",
            "password",
            "registration_date",
            "modification_date",
            "phone",
            "billing_file",
            "movie_cover",
            "is_deleted",
            "deleted_at",
            "created_by",
            "updated_by",
        ]

        labels = {"justification": FORM_JUSTIFICATION_LABEL}
        widgets = {
            "justification": forms.Textarea(
                attrs={
                    "placeholder": FORM_JUSTIFICATION_PLACEHOLDER,
                    "class": "form-control",
                }
            ),
        }
