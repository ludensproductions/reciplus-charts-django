from django import forms

from apps.comun.forms import AbstractModelForm

from .consts import VIDEO_URL_LABEL, VIDEO_URL_PLACEHOLDER
from .models import Video


class VideoForm(AbstractModelForm):
    """Form to create or update a Video instance."""

    class Meta:
        model = Video
        fields = ["video_url"]
        labels = {
            "video_url": VIDEO_URL_LABEL,
        }

        widgets = {
            "video_url": forms.TextInput(attrs={"placeholder": VIDEO_URL_PLACEHOLDER}),
        }
