from django import forms

from apps.comun.forms import (
    AbstractModelForm,
)

from .consts import FORM_THEME_LABEL, FORM_THEME_PLACEHOLDER
from .models import MusicThemes


class MusicThemesForm(AbstractModelForm):
    """Form to create or update music themes."""

    class Meta:
        model = MusicThemes
        fields = ["theme"]  # You can change this for the field"s name

        labels = {
            "theme": FORM_THEME_LABEL,
        }

        widgets = {
            "theme": forms.TextInput(attrs={"placeholder": FORM_THEME_PLACEHOLDER}),
        }
