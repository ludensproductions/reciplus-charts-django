from django import forms

from apps.comun.forms import AbstractModelForm

from .consts import FIELD_GENRE_LABEL
from .models import Genre


class GenreForm(AbstractModelForm):
    """Form for creating and editing genre records.

    This form centralizes user-facing labels and placeholders through
    application constants to preserve translation consistency.

    Attributes:
        Meta (type): Model form metadata with field, exclusion, label, and
            widget configuration.

    Side Effects:
        Renders translated labels and placeholders in form views.
    """

    class Meta:
        model = Genre
        fields = ["display_name"]
        exclude = ["genre", "is_deleted", "deleted_at", "created_by", "updated_by"]

        labels = {
            "display_name": FIELD_GENRE_LABEL,
        }

        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": FIELD_GENRE_LABEL}),
        }
