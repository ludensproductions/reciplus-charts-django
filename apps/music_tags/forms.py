from django import forms

from apps.comun.forms import (
    AbstractModelForm,
)

from .consts import FORM_TAG_LABEL, FORM_TAG_PLACEHOLDER
from .models import MusicTags


class MusicTagsForm(AbstractModelForm):
    """Form to create or update music tags."""

    class Meta:
        model = MusicTags
        fields = ["tag"]  # You can change this for the field"s name

        labels = {
            "tag": FORM_TAG_LABEL,
        }

        widgets = {
            "tag": forms.TextInput(attrs={"placeholder": FORM_TAG_PLACEHOLDER}),
        }
