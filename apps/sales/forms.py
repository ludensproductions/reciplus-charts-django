from crispy_forms.helper import FormHelper
from django import forms
from django.forms import BaseFormSet, BaseInlineFormSet

from apps.comun.forms import AbstractModelForm
from apps.movies.models import MovieSales

from .consts import (
    ERROR_AT_LEAST_ONE_MOVIE,
    ERROR_DUPLICATE_MOVIE,
    FORM_MOVIE_LABEL,
    FORM_MOVIE_PLACEHOLDER,
    FORM_QUANTITY_LABEL,
    FORM_QUANTITY_PLACEHOLDER,
    FORM_SALE_NAME_LABEL,
    FORM_SALE_NAME_PLACEHOLDER,
)
from .models import Sale


class SaleForm(AbstractModelForm):
    """Form for creating or updating a sale header."""

    class Meta:
        model = Sale
        fields = ["name"]  # You can change this for the field's name
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]

        labels = {
            "name": FORM_SALE_NAME_LABEL,
        }

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": FORM_SALE_NAME_PLACEHOLDER}),
        }


class MovieSalesForm(AbstractModelForm):
    """Form for adding a movie and quantity to a sale."""

    class Meta:
        model = MovieSales
        fields = ["movie", "quantity"]  # You can change this for the field's name
        exclude = ["is_deleted", "deleted_at", "sale", "created_by", "updated_by"]

        labels = {
            "movie": FORM_MOVIE_LABEL,
            "quantity": FORM_QUANTITY_LABEL,
        }
        widgets = {
            "movie": forms.Select(
                attrs={"placeholder": FORM_MOVIE_PLACEHOLDER, "class": "input_formset"},
            ),
            "quantity": forms.NumberInput(attrs={"placeholder": FORM_QUANTITY_PLACEHOLDER, "class": "input_formset"}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form helper and required fields."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.fields["movie"].required = True


class BaseASaleFormSet(BaseFormSet):
    """Formset for validating sale items in standalone forms."""

    def clean(self):
        """Validate unique movies and at least one item.

        Raises:
            ValidationError: When duplicate movies exist or no items are provided.
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        movies = []
        valid_forms = 0

        for form in self.forms:
            valid_forms += 1
            movie = form.cleaned_data.get("movie")
            if movie in movies:
                form.errors["movie"] = form.error_class([ERROR_DUPLICATE_MOVIE])
                # raise ValidationError("Articles in a set must have distinct titles.")
            movies.append(movie)

        if valid_forms < 1:
            raise forms.ValidationError(ERROR_AT_LEAST_ONE_MOVIE)


class BaseSaleInlineFormSet(BaseInlineFormSet):
    """Inline formset for validating sale items within a parent sale."""

    def clean(self):
        """Validate unique movies and at least one item.

        Raises:
            ValidationError: When duplicate movies exist or no items are provided.
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        movies = []
        valid_forms = 0

        for form in self.forms:
            valid_forms += 1
            movie = form.cleaned_data.get("movie")
            if movie in movies:
                form.errors["movie"] = form.error_class([ERROR_DUPLICATE_MOVIE])
            movies.append(movie)

        if valid_forms < 1:
            raise forms.ValidationError(ERROR_AT_LEAST_ONE_MOVIE)
