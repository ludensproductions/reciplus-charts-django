from django import forms

from apps.comun.forms import (
    AbstractModelForm,
)

from .consts import FORM_GENRE_LABEL, FORM_GENRE_PLACEHOLDER
from .models import MusicGenres


class MusicGenresForm(AbstractModelForm):
    """Form to create or update music genres."""

    class Meta:
        model = MusicGenres
        fields = ["genre"]  # You can change this for the field"s name

        labels = {
            "genre": FORM_GENRE_LABEL,
        }

        widgets = {
            "genre": forms.TextInput(attrs={"placeholder": FORM_GENRE_PLACEHOLDER}),
        }
