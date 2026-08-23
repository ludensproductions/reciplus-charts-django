from django import forms

from apps.comun.forms import AbstractModelForm

from . import consts as contents_consts
from .models import Content


class ContentForm(AbstractModelForm):
    """Form for creating and updating content entries."""

    class Meta:
        model = Content
        fields = ["title", "content_type"]

        labels = {
            "title": contents_consts.CONTENT_FORM_TITLE_LABEL,
            "content_type": contents_consts.CONTENT_FORM_TYPE_LABEL,
        }

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": contents_consts.CONTENT_TITLE_PLACEHOLDER}),
        }
