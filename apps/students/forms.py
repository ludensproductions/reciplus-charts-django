from django import forms

from apps.comun.forms import AbstractModelForm

from .consts import (
    STUDENT_ADDRESS_LABEL,
    STUDENT_EMAIL_LABEL,
    STUDENT_IMAGE_LABEL,
    STUDENT_LAST_NAME_LABEL,
    STUDENT_NAME_LABEL,
    STUDENT_PHONE_LABEL,
)
from .models import Student


class StudentForm(AbstractModelForm):
    """Form for creating and editing student records.

    This form centralizes student field labels and placeholders using
    i18n-ready constants defined at the app level.

    Attributes:
        Meta (type): Model form configuration for editable fields, labels,
            and widgets.

    Side Effects:
        Renders translated labels and placeholders in form templates.
    """

    class Meta:
        model = Student
        fields = ["name", "last_name", "email", "phone", "address", "image"]
        labels = {
            "name": STUDENT_NAME_LABEL,
            "last_name": STUDENT_LAST_NAME_LABEL,
            "email": STUDENT_EMAIL_LABEL,
            "phone": STUDENT_PHONE_LABEL,
            "address": STUDENT_ADDRESS_LABEL,
            "image": STUDENT_IMAGE_LABEL,
        }

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": STUDENT_NAME_LABEL}),
            "last_name": forms.TextInput(attrs={"placeholder": STUDENT_LAST_NAME_LABEL}),
            "email": forms.EmailInput(attrs={"placeholder": STUDENT_EMAIL_LABEL}),
            "phone": forms.TextInput(attrs={"placeholder": STUDENT_PHONE_LABEL}),
            "address": forms.TextInput(attrs={"placeholder": STUDENT_ADDRESS_LABEL}),
            "image": forms.ClearableFileInput(attrs={"placeholder": STUDENT_IMAGE_LABEL}),
        }
