from django import forms

from apps.categories import consts
from apps.comun.forms import AbstractModelForm

from .models import Category


class CategoryForm(AbstractModelForm):
    """Form for creating and editing Category instances.

    Uses centralized, internationalized labels and placeholders from app constants.
    """

    class Meta:
        model = Category
        fields = ["name"]
        labels = {
            "name": consts.INDEX_FIELDS["name"],
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": consts.FILTER_FIELDS["name"]["placeholder"]}),
        }
