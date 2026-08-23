import re

from django import forms
from django.contrib.auth.models import Permission

from apps.comun.forms import AbstractModelForm

from .consts import ERROR_GROUP_EXISTS, ERROR_GROUP_INVALID, FORM_GROUP_LABEL, FORM_GROUP_PLACEHOLDER
from .models import CustomGroup


class GroupForm(AbstractModelForm):
    """Form for creating or updating authorization groups."""

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
    )
    code_attr = "name"

    class Meta:
        model = CustomGroup
        fields = ["display_name"]
        labels = {"display_name": FORM_GROUP_LABEL}
        widgets = {
            "display_name": forms.TextInput(
                attrs={"data-name": FORM_GROUP_LABEL, "placeholder": FORM_GROUP_PLACEHOLDER}
            )
        }

    def clean_display_name(self):
        """Validate group display name uniqueness and format.

        Returns:
            str: Validated display name.

        Raises:
            ValidationError: When name exists or fails validation.
        """
        name = self.cleaned_data["display_name"]

        if CustomGroup.objects.filter(display_name__iexact=name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(ERROR_GROUP_EXISTS)

        if not self.validate_text(name):
            raise forms.ValidationError(ERROR_GROUP_INVALID)

        return name

    def validate_text(self, value):
        """Validate allowed characters for group names.

        Args:
            value (str): Text to validate.

        Returns:
            Match | None: Regex match when valid.
        """
        # Regex for validating characters, spaces, numbers, accents and commas
        regex = re.compile(r"^[a-zA-ZÀ-ÿ0-9ñÑ\s(),.]+$")
        return regex.match(value)

    def save(self, commit=True):
        """Persist group and assign permissions.

        Args:
            commit (bool): When True, saves the group instance.

        Returns:
            CustomGroup: Saved group instance.
        """
        instance = super().save(commit=False)
        display_name_attr = "display_name"
        if display_name_attr and self.code_attr:
            display_name = getattr(instance, display_name_attr)

            filters = {self.code_attr: display_name}
            repeated_instances = CustomGroup.all_objects.filter(**filters)
            if not repeated_instances.exists():
                setattr(instance, self.code_attr, display_name)
            else:
                filters = {display_name_attr + "__startswith": display_name}
                counter = CustomGroup.all_objects.filter(**filters).count() + 1
                new_display_name = display_name + "_" + str(counter)
                setattr(instance, self.code_attr, new_display_name)
        instance.save()
        instance.permissions.set(self.cleaned_data["permissions"])
        return instance
