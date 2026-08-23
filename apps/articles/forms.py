from django import forms

from apps.comun.forms import (
    AbstractModelForm,
)

from .consts import BODY_LABEL, CATEGORY_LABEL
from .models import Article


class ArticleForm(AbstractModelForm):
    """Model form for creating and updating article records.

    This form defines the editable fields for the articles domain and
    centralizes user-facing labels/placeholders through app constants to
    preserve internationalization consistency.

    Attributes:
        Meta (type): Django metadata configuring model binding, fields,
            labels, and widgets.

    Side Effects:
        Renders translated labels and placeholders in templates/forms.
    """

    class Meta:
        model = Article
        fields = ["body", "category"]

        labels = {
            "body": BODY_LABEL,
            "category": CATEGORY_LABEL,
        }

        widgets = {
            "body": forms.TextInput(attrs={"placeholder": BODY_LABEL}),
        }
