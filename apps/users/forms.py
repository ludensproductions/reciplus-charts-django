import re

from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from django.forms.models import ModelChoiceIterator
from django.utils.safestring import mark_safe
from unidecode import unidecode

from apps.comun.consts import ERROR_REQUIRED_FIELD
from apps.comun.forms import AbstractModelForm
from apps.comun.select2.widgets import BaseModelSelect2Widget, ModelSelect2SingleTagWidget
from apps.departments.forms import GroupsWidget
from apps.departments.models import Departamento
from apps.groups.models import CustomGroup
from apps.positions.models import Puesto
from apps.users.models import CodigoPostal, Domicilio, Estado, Municipio, User

from .consts import (
    ERROR_EMAIL_TAKEN,
    ERROR_INVALID_EMAIL,
    ERROR_INVALID_IMAGE,
    ERROR_INVALID_IMAGE_EXTENSION,
    ERROR_INVALID_MUNICIPIO,
    ERROR_INVALID_POSTAL_CODE,
    ERROR_PASSWORD_FIELDS_REQUIRED,
    ERROR_PASSWORD_MIN_LENGTH,
    ERROR_PASSWORD_MISMATCH,
    ERROR_PASSWORD_SPECIAL_CHAR,
    ERROR_USER_EMAIL_EXISTS,
    ERROR_USERNAME_TAKEN,
    FORGOT_PASSWORD_EMAIL_PLACEHOLDER,
    FORM_DOMICILIO_CALLE_LABEL,
    FORM_DOMICILIO_CALLE_PLACEHOLDER,
    FORM_DOMICILIO_CODIGO_POSTAL_LABEL,
    FORM_DOMICILIO_COLONIA_LABEL,
    FORM_DOMICILIO_COLONIA_PLACEHOLDER,
    FORM_DOMICILIO_ESTADO_LABEL,
    FORM_DOMICILIO_MUNICIPIO_LABEL,
    FORM_DOMICILIO_NUMERO_EXTERIOR_LABEL,
    FORM_DOMICILIO_NUMERO_EXTERIOR_PLACEHOLDER,
    FORM_DOMICILIO_NUMERO_INTERIOR_LABEL,
    FORM_DOMICILIO_NUMERO_INTERIOR_PLACEHOLDER,
    FORM_GROUPS_LABEL,
    FORM_GROUPS_PLACEHOLDER,
    FORM_NEW_USER_EMAIL_PLACEHOLDER,
    FORM_NEW_USER_FIRST_NAME_PLACEHOLDER,
    FORM_NEW_USER_LAST_NAME_PLACEHOLDER,
    FORM_NEW_USER_PASSWORD_CONFIRM_LABEL,
    FORM_NEW_USER_PASSWORD_LABEL,
    FORM_NEW_USER_PASSWORD_PLACEHOLDER,
    FORM_NEW_USER_USERNAME_PLACEHOLDER,
    FORM_PROFILE_EMAIL_LABEL_HTML,
    FORM_PROFILE_EMAIL_PLACEHOLDER,
    FORM_PROFILE_PASSWORD_CONFIRM_LABEL,
    FORM_PROFILE_PASSWORD_CONFIRM_LABEL_HTML,
    FORM_PROFILE_PASSWORD_CONFIRM_PLACEHOLDER,
    FORM_PROFILE_PASSWORD_LABEL,
    FORM_PROFILE_PASSWORD_LABEL_HTML,
    FORM_PROFILE_PASSWORD_PLACEHOLDER,
    FORM_USER_DEPARTAMENTO_LABEL,
    FORM_USER_EMAIL_LABEL,
    FORM_USER_FIRST_NAME_LABEL,
    FORM_USER_HAS_DOMICILE_LABEL,
    FORM_USER_LAST_NAME_LABEL,
    FORM_USER_MOBILE_LABEL,
    FORM_USER_PUESTO_LABEL,
    FORM_USER_SECOND_LAST_NAME_LABEL,
    FORM_USER_WORK_PHONE_LABEL,
    LABEL_EMAIL,
    LABEL_NEW_PASSWORD,
    LABEL_REPEAT_PASSWORD,
    MSG_EMAIL_INVALID,
    MSG_FIELD_REQUIRED,
    PASSWORD_ERROR_MISMATCH,
    PASSWORD_VALIDATION_ERROR_MAP,
    PLACEHOLDER_NEW_PASSWORD,
    PLACEHOLDER_REPEAT_PASSWORD,
    USER_USERNAME_RESERVED_SUFFIX_ERROR,
)
from .utils import (
    get_available_username_input_max_length,
    is_valid_mail,
    send_password_reset_email,
)


class EditProfileForm(forms.ModelForm):
    """Form to update user profile data and optional password/image."""

    image = forms.FileField(
        label="",
        widget=forms.ClearableFileInput(),
        required=False,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "svg"])],
        error_messages={
            "invalid_image": ERROR_INVALID_IMAGE,
            "invalid_extension": ERROR_INVALID_IMAGE_EXTENSION,
        },
    )

    password = forms.CharField(
        label=FORM_PROFILE_PASSWORD_LABEL,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "password",
                "id": "password",
                "placeholder": FORM_PROFILE_PASSWORD_PLACEHOLDER,
            }
        ),
    )

    password2 = forms.CharField(
        required=False,
        label=FORM_PROFILE_PASSWORD_CONFIRM_LABEL,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": FORM_PROFILE_PASSWORD_CONFIRM_PLACEHOLDER,
                "id": "verifyPassword",
            }
        ),
    )

    class Meta:
        model = User

        # Define the fields that will be displayed on the form with their DB column names
        fields = [
            "email",
            "password",
            "password2",
            "image",
        ]

        # exclude = ('first_name', 'last_name', 'city', 'state', 'username', 'country', 'address')

        # Modify any labels here if required
        labels = {
            # mark_safe to prevent XSS attacks
            "image": mark_safe(""),  # Clean the image label
            "email": mark_safe(FORM_PROFILE_EMAIL_LABEL_HTML),
            "password": mark_safe(FORM_PROFILE_PASSWORD_LABEL_HTML),
            "password2": mark_safe(FORM_PROFILE_PASSWORD_CONFIRM_LABEL_HTML),
        }

        # Modify the input attributes
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "name": "email",
                    "id": "email",
                    "placeholder": FORM_PROFILE_EMAIL_PLACEHOLDER,
                    "required": "",
                }
            ),
        }

    def clean_email(self):
        """Validate the email format.

        Returns:
            str: Normalized email value.

        Raises:
            ValidationError: When the email format is invalid.
        """
        email = self.cleaned_data.get("email", None)
        # check regex for email
        if not is_valid_mail(email):
            raise ValidationError(ERROR_INVALID_EMAIL)
        return email

    def clean(self):
        """Validate password fields and enforce password rules.

        Returns:
            dict: Cleaned form data.

        Raises:
            ValidationError: When password rules or matching fail.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password", "").strip()
        password2 = cleaned_data.get("password2", "").strip()

        if not password and not password2:
            return cleaned_data

        if bool(password) != bool(password2):
            raise ValidationError(
                {
                    "password": ERROR_PASSWORD_FIELDS_REQUIRED,
                    "password2": ERROR_PASSWORD_FIELDS_REQUIRED,
                }
            )

        if password or password2:
            if not password or not password2:
                raise ValidationError(
                    {
                        "password": ERROR_PASSWORD_FIELDS_REQUIRED,
                        "password2": ERROR_PASSWORD_FIELDS_REQUIRED,
                    }
                )

            if password != password2:
                raise ValidationError({"password2": ERROR_PASSWORD_MISMATCH})

            if len(password) < 8:
                raise ValidationError({"password": ERROR_PASSWORD_MIN_LENGTH})

            if not any(c in '!@#$%^&*(),.?":{}|<>' for c in password):
                raise ValidationError({"password": ERROR_PASSWORD_SPECIAL_CHAR})

        return cleaned_data

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super(EditProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Persist user changes and update password or image when provided.

        Args:
            commit (bool): When True, saves the user instance.

        Returns:
            User: Updated user instance.
        """
        user = super(EditProfileForm, self).save(commit=False)
        password = self.cleaned_data.get("password", "").strip()

        # Update password only if a new one is provided and passes validation
        if password:
            # Ensure it passed clean() validation
            if "password2" in self.cleaned_data and password == self.cleaned_data["password2"].strip():
                user.set_password(password)
        else:
            # Preserve existing password
            actual_user = User.objects.get(id=user.id)
            user.password = actual_user.password

        # Process image if a new one is provided
        image = self.cleaned_data.get("image")
        if image:
            try:
                image_name = image.name.replace(" ", "_")
                # Regex that ignores single and double quotes
                image_name = re.sub(r'[\'"]', "", image_name)
                image_name = unidecode(image_name)
                user.image.name = image_name
            except AttributeError:
                user.image.name = "profiles/generic/default_profile.jpeg"

        if commit:
            user.save()
        return user


class NewUserForm(UserCreationForm):
    """User creation form with username, email, and password fields."""

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": FORM_NEW_USER_EMAIL_PLACEHOLDER, "id": "email"}),
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": FORM_NEW_USER_USERNAME_PLACEHOLDER}),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": FORM_NEW_USER_PASSWORD_PLACEHOLDER,
                "type": "password",
                "minlength": 8,
                "id": "password",
            }
        ),
        required=True,
        label=FORM_NEW_USER_PASSWORD_LABEL,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": FORM_NEW_USER_PASSWORD_PLACEHOLDER,
                "type": "password",
                "minlength": 8,
                "id": "verifyPassword",
            }
        ),
        required=True,
        label=FORM_NEW_USER_PASSWORD_CONFIRM_LABEL,
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": FORM_NEW_USER_FIRST_NAME_PLACEHOLDER}),
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": FORM_NEW_USER_LAST_NAME_PLACEHOLDER}),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )

    def save(self, commit=True):
        """Persist a new user with the provided email.

        Args:
            commit (bool): When True, saves the user instance.

        Returns:
            User: Created user instance.
        """
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_username(self):
        """Validate that the username is not already taken.

        Returns:
            str: Username value.

        Raises:
            ValidationError: When the username already exists.
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError(ERROR_USERNAME_TAKEN)
        return username

    def clean_email(self):
        """Validate that the email is not already taken.

        Returns:
            str: Email value.

        Raises:
            ValidationError: When the email already exists.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(ERROR_EMAIL_TAKEN)
        return email

    def __init__(self, *args, **kwargs):
        """Initialize form and apply Bootstrap styling to all visible fields.

        Args:
            *args: Additional positional arguments passed to parent class.
            **kwargs: Additional keyword arguments passed to parent class.
        """
        super(NewUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control form-control-user"


class DepartamentoSelect2Widget(BaseModelSelect2Widget):
    """Select2 widget for department lookup."""

    model = Departamento
    search_fields = ["nombre_departamento__icontains"]  # search fields for the select2 widget

    def label_from_instance(self, obj):
        """Method that returns the label of the instance.

        Args:
            obj (Any): Instance of the model

        Returns:
            Any: Label of the instance
        """
        return obj.nombre_departamento

    def __init__(self, *args, **kwargs):
        """Configure the widget data source."""
        kwargs["data_view"] = "users:user_select2"  # url to get the data
        super().__init__(*args, **kwargs)


class PuestoSelect2Widget(BaseModelSelect2Widget):
    """Select2 widget for position lookup with department dependency."""

    model = Puesto
    search_fields = ["puesto__icontains"]  # search fields for the select2 widget
    dependent_fields = {"departamento": "puesto_departamento__departamento"}
    require_dependencies = True

    def label_from_instance(self, obj):
        """Method that returns the label of the instance.

        Args:
            obj (Any): Instance of the model

        Returns:
            Any: Label of the instance
        """
        return obj.puesto

    def get_queryset(self):
        """Filter positions to exclude deleted department links.

        Returns:
            QuerySet: Filtered positions.
        """
        return super().get_queryset().filter(puesto_departamento__deleted__isnull=True)


class UserForm(AbstractModelForm):
    """Base user form used in profile or admin flows."""

    has_domicile = forms.BooleanField(
        label=FORM_USER_HAS_DOMICILE_LABEL,
        widget=forms.HiddenInput(),
        required=False,
        initial=False,
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "second_last_name",
            "email",
            "celular",
            "telefono_trabajo",
            "departamento",
            "puesto",
        ]

        labels = {
            "first_name": FORM_USER_FIRST_NAME_LABEL,
            "last_name": FORM_USER_LAST_NAME_LABEL,
            "second_last_name": FORM_USER_SECOND_LAST_NAME_LABEL,
            "email": FORM_USER_EMAIL_LABEL,
            "celular": FORM_USER_MOBILE_LABEL,
            "telefono_trabajo": FORM_USER_WORK_PHONE_LABEL,
            "departamento": FORM_USER_DEPARTAMENTO_LABEL,
            "puesto": FORM_USER_PUESTO_LABEL,
        }

        widgets = {
            "departamento": DepartamentoSelect2Widget(attrs={"class": "form-control"}),
            "puesto": PuestoSelect2Widget(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form and add placeholders from labels."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["placeholder"] = self._meta.labels.get(field_name)

        email_value = self.instance.email if self.instance and self.instance.pk else ""
        max_length = get_available_username_input_max_length(email_value)
        self.fields["email"].max_length = max_length
        self.fields["email"].widget.attrs["maxlength"] = max_length

    def clean_email(self):
        """Validate email uniqueness among active users.

        Returns:
            str: Lowercased email value.

        Raises:
            ValidationError: When the email already exists.
        """
        email = self.cleaned_data["email"].lower()
        max_length = get_available_username_input_max_length(email)

        if len(email) > max_length:
            raise ValidationError(USER_USERNAME_RESERVED_SUFFIX_ERROR.format(max_length=max_length))

        users = User.all_objects.filter(email=email, deleted__isnull=True)

        if self.instance.pk:
            users = users.exclude(pk=self.instance.pk)

        if users.exists():
            raise ValidationError(ERROR_USER_EMAIL_EXISTS)
        return email


class EstadoSelect2Widget(BaseModelSelect2Widget):
    """Select2 widget for Mexican states."""

    model = Estado
    search_fields = ["estado__icontains"]  # search fields for the select2 widget

    def label_from_instance(self, obj):
        """Method that returns the label of the instance.

        Args:
            obj (Any): Instance of the model

        Returns:
            Any: Label of the instance
        """
        return obj.estado

    def get_queryset(self):
        """Return states scoped to Mexico and ordered by name.

        Returns:
            QuerySet: Filtered states.
        """
        return super().get_queryset().filter(pais__clave="MEX").order_by("estado")


class MunicipioSelect2Widget(BaseModelSelect2Widget):
    """Select2 widget for municipalities with state dependency."""

    model = Municipio
    search_fields = ["municipio__icontains"]  # search fields for the select2 widget
    dependent_fields = {"domicilio-estado": "estado"}
    require_dependencies = True

    def label_from_instance(self, obj):
        """Method that returns the label of the instance.

        Args:
            obj (Any): Instance of the model

        Returns:
            Any: Label of the instance
        """
        return obj.municipio

    def get_queryset(self):
        """Return municipalities ordered by name.

        Returns:
            QuerySet: Ordered municipalities.
        """
        return super().get_queryset().order_by("municipio")


class CodigoPostalSelect2Widget(ModelSelect2SingleTagWidget):
    """Select2 widget for postal codes with municipality dependency."""

    model = CodigoPostal
    search_fields = ["codigo_postal__icontains"]  # search fields for the select2 widget
    dependent_fields = {"domicilio-municipio": "municipio", "domicilio-estado": "municipio__estado"}
    require_dependencies = True

    def label_from_instance(self, obj):
        """Method that returns the label of the instance.

        Args:
            obj (Any): Instance of the model

        Returns:
            Any: Label of the instance
        """
        return obj.codigo_postal

    def get_queryset(self):
        """Return postal codes for select2 queries.

        Returns:
            QuerySet: Postal code queryset.
        """
        return super().get_queryset()

    def optgroups(self, name, value, attrs=None):
        """Return only selected options and set QuerySet from `ModelChoicesIterator`.

        Args:
            name (str): Field name.
            value (list[str]): Current values.
            attrs (dict | None): Optional widget attributes.

        Returns:
            list: Optgroups rendered for select2.
        """
        default = (None, [], 0)
        groups = [default]
        has_selected = False
        field_name = self.choices.field.to_field_name or "pk"
        selected_choices = {str(v) for v in value if field_name != "pk" or str(v).isnumeric()}
        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, "", "", False, 0))
        if not isinstance(self.choices, ModelChoiceIterator):
            return super().optgroups(name, value, attrs=attrs)
        selected_choices = {c for c in selected_choices if c not in self.choices.field.empty_values}
        query = Q(**{"%s__in" % field_name: selected_choices})
        for obj in self.choices.queryset.filter(query):
            option_value = self.choices.choice(obj)[0]
            option_label = self.label_from_instance(obj)

            selected = str(option_value) in value and (has_selected is False or self.allow_multiple_selected)
            if selected is True and has_selected is False:
                has_selected = True
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(self.create_option(name, option_value, option_label, selected_choices, index))
        return groups


class ForgotPasswordForm(forms.Form):
    """Form for forgot password email input."""

    email = forms.EmailField(
        label=LABEL_EMAIL,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "email",
                "name": "email",
                "placeholder": FORGOT_PASSWORD_EMAIL_PLACEHOLDER,
            }
        ),
        error_messages={"required": MSG_FIELD_REQUIRED, "invalid": MSG_EMAIL_INVALID},
    )


class CustomSetPasswordForm(SetPasswordForm):
    """Set password form with custom-styled inputs and Spanish error messages."""

    error_messages = {
        "password_mismatch": PASSWORD_ERROR_MISMATCH,
    }

    new_password1 = forms.CharField(
        label=LABEL_NEW_PASSWORD,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "autocomplete": "new-password",
                "placeholder": PLACEHOLDER_NEW_PASSWORD,
            }
        ),
    )
    new_password2 = forms.CharField(
        label=LABEL_REPEAT_PASSWORD,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "autocomplete": "new-password",
                "placeholder": PLACEHOLDER_REPEAT_PASSWORD,
            }
        ),
    )

    def _post_clean(self):
        """Replaces password validator errors with translated messages."""
        super()._post_clean()
        if "new_password2" in self._errors:
            translated = []
            for error in self._errors["new_password2"].as_data():
                msg = PASSWORD_VALIDATION_ERROR_MAP.get(error.code)
                if msg:
                    translated.append(ValidationError(msg, code=error.code, params=error.params))
                else:
                    translated.append(error)
            self._errors["new_password2"] = self.error_class(translated)


class CustomPasswordResetForm(PasswordResetForm):
    """Password reset form with soft-delete aware user lookup."""

    email = forms.EmailField(
        label=LABEL_EMAIL,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "email",
                "name": "email",
                "placeholder": FORGOT_PASSWORD_EMAIL_PLACEHOLDER,
            }
        ),
        error_messages={"required": MSG_FIELD_REQUIRED, "invalid": MSG_EMAIL_INVALID},
    )

    def get_users(self, email):
        """Return active, non-deleted users matching the given email."""
        active_users = User._default_manager.filter(
            email__iexact=email,
            is_active=True,
            deleted__isnull=True,
        )
        return (u for u in active_users if u.has_usable_password())

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """Delegate password reset email delivery to the users utility module."""
        send_password_reset_email(
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name,
        )


class ModelChoiceCodigoPostal(forms.ModelChoiceField):
    """ModelChoiceField that allows creating new postal code values."""

    def to_python(self, value):
        """Convert raw form value into a postal code or model instance.

        Handles both new postal codes (prefixed with "new_") and existing
        instances. Validates new postal codes as 5-digit numbers and resolves
        existing codes by primary key.

        Args:
            value (str | None): Raw form value.

        Returns:
            CodigoPostal | str: Existing instance or new postal code string.

        Raises:
            ValidationError: When the value is invalid or doesn't meet postal
                code format requirements.
        """
        if not value:
            raise ValidationError(ERROR_REQUIRED_FIELD)

        if value.startswith("new_"):
            value = value[4:]
            # Validate that the value is exactly 5 numeric digits
            if not re.match(r"^\d{5}$", value):
                raise ValidationError(
                    self.error_messages["invalid_choice"],
                    code="invalid_choice",
                    params={"value": value},
                )
            return value
        # If it's an existing value, verify it's a valid ID
        try:
            value = int(value)
            value = self.queryset.model.objects.get(pk=value)
        except self.queryset.model.DoesNotExist:
            raise ValidationError(ERROR_INVALID_POSTAL_CODE)
        except self.queryset.model.MultipleObjectsReturned:
            raise ValidationError(ERROR_INVALID_POSTAL_CODE)

        except (ValueError, TypeError):
            raise ValidationError(ERROR_INVALID_POSTAL_CODE)

        return value


class DomicilioForm(forms.ModelForm):
    """Form to capture or update domicile data."""

    estado = forms.ModelChoiceField(
        label=FORM_DOMICILIO_ESTADO_LABEL,
        queryset=Estado.objects.all(),
        widget=EstadoSelect2Widget(attrs={"class": "form-control"}),
        required=False,
    )

    codigo_postal = ModelChoiceCodigoPostal(
        label=FORM_DOMICILIO_CODIGO_POSTAL_LABEL,
        queryset=CodigoPostal.objects.all(),
        widget=CodigoPostalSelect2Widget(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Domicilio
        fields = ["estado", "municipio", "colonia", "codigo_postal", "calle", "numero_exterior", "numero_interior"]

        labels = {
            "municipio": FORM_DOMICILIO_MUNICIPIO_LABEL,
            "colonia": FORM_DOMICILIO_COLONIA_LABEL,
            "calle": FORM_DOMICILIO_CALLE_LABEL,
            "numero_exterior": FORM_DOMICILIO_NUMERO_EXTERIOR_LABEL,
            "numero_interior": FORM_DOMICILIO_NUMERO_INTERIOR_LABEL,
        }

        widgets = {
            "estado": EstadoSelect2Widget(attrs={"class": "form-control"}),
            "municipio": MunicipioSelect2Widget(attrs={"class": "form-control"}),
            "colonia": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "name": "colonia",
                    "placeholder": FORM_DOMICILIO_COLONIA_PLACEHOLDER,
                }
            ),
            "codigo_postal": CodigoPostalSelect2Widget(attrs={"class": "form-control"}),
            "calle": forms.TextInput(
                attrs={"class": "form-control", "name": "calle", "placeholder": FORM_DOMICILIO_CALLE_PLACEHOLDER}
            ),
            "numero_exterior": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "name": "numero_exterior",
                    "placeholder": FORM_DOMICILIO_NUMERO_EXTERIOR_PLACEHOLDER,
                }
            ),
            "numero_interior": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "name": "numero_interior",
                    "placeholder": FORM_DOMICILIO_NUMERO_INTERIOR_PLACEHOLDER,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form and configure required field flags.

        Sets all form fields as optional by default. If editing an existing
        instance, initializes the estado field with the municipality's state.

        Args:
            *args: Additional positional arguments passed to parent class.
            **kwargs: Additional keyword arguments passed to parent class.
        """
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        for fields in self.fields:
            self.fields[fields].required = False

        if self.instance and self.instance.pk:
            self.initial["estado"] = self.instance.municipio.estado.id

    def clean_codigo_postal(self):
        """Validate and create postal codes when needed.

        Checks if the postal code is an instance of CodigoPostal. If not,
        validates that the municipality is selected and creates a new postal
        code entry if necessary.

        Returns:
            CodigoPostal: Selected or newly created postal code instance.

        Raises:
            ValidationError: When postal code or municipality is invalid.
        """
        codigo_postal = self.cleaned_data.get("codigo_postal")

        # Return if postal code is already a CodigoPostal instance
        if isinstance(codigo_postal, CodigoPostal):
            return codigo_postal

        domicilio_municipio = self.cleaned_data.get("municipio")

        if not codigo_postal:
            raise ValidationError(ERROR_REQUIRED_FIELD)

        if not domicilio_municipio:
            raise ValidationError(ERROR_INVALID_MUNICIPIO)

        codigo_postal = CodigoPostal.objects.create(
            codigo_postal=codigo_postal,
            municipio=domicilio_municipio,
        )

        return codigo_postal


class GroupsUserForm(forms.Form):
    """Form for assigning authorization groups to a user."""

    auth_group = forms.ModelMultipleChoiceField(
        queryset=CustomGroup.objects.all(),
        label=FORM_GROUPS_LABEL,
        required=False,
        widget=GroupsWidget(
            attrs={
                "data-minimum-input-length": "0",
                "class": "form-control",
                "data-allow-clear": "true",
                "data-placeholder": FORM_GROUPS_PLACEHOLDER,
            }
        ),
    )
