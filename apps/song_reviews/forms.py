from django import forms

from apps.albums.models import Album, Song
from apps.comun.forms import AbstractModelForm
from apps.comun.select2.widgets import BaseModelSelect2Widget

from .consts import (
    FORM_ALBUM_LABEL,
    FORM_REVIEW_LABEL,
    FORM_REVIEW_PLACEHOLDER,
    FORM_SCORE_LABEL,
    FORM_SCORE_PLACEHOLDER,
    FORM_SONG_LABEL,
)
from .models import SongReview


class SongSelect2Widget(BaseModelSelect2Widget):
    """Select2 widget configuration for song lookups."""

    model = Song
    search_fields = ["title__icontains"]  # Search fields for the Select2 widget.

    def label_from_instance(self, obj):
        """Return the display label for a Song instance.

        Args:
            obj (Any): Song model instance.

        Returns:
            Any: The label displayed in Select2.
        """
        return obj.title

    def __init__(self, *args, **kwargs):
        """Initialize widget and bind the Select2 data source route."""
        kwargs["data_view"] = "song_reviews:song_select2"  # URL used to fetch Select2 data.
        super().__init__(*args, **kwargs)


class AlbumSelect2Widget(BaseModelSelect2Widget):
    """Select2 widget configuration for album lookups."""

    model = Album
    search_fields = ["title__icontains"]  # Search fields for the Select2 widget.

    def label_from_instance(self, obj):
        """Return the display label for an Album instance.

        Args:
            obj (Any): Album model instance.

        Returns:
            Any: The label displayed in Select2.
        """
        return obj.title


class SongReviewForm(AbstractModelForm):
    """Form used to create and update song review records.

    This form binds review fields and centralizes all user-facing labels and
    placeholders through app-level i18n constants.
    """

    class Meta:
        model = SongReview
        fields = [
            "album",
            "song",
            "score",
            "review",
        ]
        exclude = ["genre", "is_deleted", "deleted_at", "created_by", "updated_by"]

        labels = {
            "album": FORM_ALBUM_LABEL,
            "song": FORM_SONG_LABEL,
            "score": FORM_SCORE_LABEL,
            "review": FORM_REVIEW_LABEL,
        }

        widgets = {
            # Parent and child widgets are both Select2; child resets on parent change.
            "album": AlbumSelect2Widget(attrs={"class": "form-control"}),
            "song": SongSelect2Widget(attrs={"class": "form-control"}, dependent_fields={"album": "album"}),
            "score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 10,
                    "placeholder": FORM_SCORE_PLACEHOLDER,
                }
            ),
            "review": forms.Textarea(attrs={"class": "form-control", "placeholder": FORM_REVIEW_PLACEHOLDER}),
        }
