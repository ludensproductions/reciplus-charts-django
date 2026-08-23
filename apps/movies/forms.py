from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms

from apps.comun.filter_fields import TruncatedModelChoiceField
from apps.comun.forms import AbstractModelForm
from apps.movies.consts import (
    DISABLE_EDIT_FIELDS,
    ERROR_MOVIE_PRICE_NEGATIVE,
    ERROR_MOVIE_YEAR_MIN,
    FORM_GENRE_LABEL,
    FORM_PLOT_LABEL,
    FORM_PLOT_PLACEHOLDER,
    FORM_PRICE_LABEL,
    FORM_PRICE_PLACEHOLDER,
    FORM_TITLE_LABEL,
    FORM_TITLE_PLACEHOLDER,
    FORM_YEAR_LABEL,
    FORM_YEAR_PLACEHOLDER,
)

from .models import Genre, Movie


class InventarioForm(AbstractModelForm):
    """Form for creating or updating movie inventory data."""

    genre = TruncatedModelChoiceField(
        queryset=Genre.objects.all(),
        required=True,
        label=FORM_GENRE_LABEL,
    )

    class Meta:
        model = Movie
        fields = ["title", "year", "genre", "price", "plot"]
        exclude = ["is_deleted", "deleted_at", "created_by", "updated_by"]
        labels = {
            "title": FORM_TITLE_LABEL,
            "year": FORM_YEAR_LABEL,
            "genre": FORM_GENRE_LABEL,
            "plot": FORM_PLOT_LABEL,
            "price": FORM_PRICE_LABEL,
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": FORM_TITLE_PLACEHOLDER}),
            "year": forms.NumberInput(attrs={"placeholder": FORM_YEAR_PLACEHOLDER}),
            "price": forms.NumberInput(attrs={"placeholder": FORM_PRICE_PLACEHOLDER, "step": 0.25}),
            "plot": forms.Textarea(attrs={"placeholder": FORM_PLOT_PLACEHOLDER, "class": "col-12"}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form layout and disable fields on edit."""
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="form-group col-md-3 mb-3"),
                Column("year", css_class="form-group col-md-3 mb-3"),
                Column("genre", css_class="form-group col-md-3 mb-3"),
                Column("price", css_class="form-group col-md-3 mb-3"),
            ),
            Row(
                Column("plot", css_class="form-group col-12 mb-3"),
            ),
        )

        if self.instance.pk:
            for field in DISABLE_EDIT_FIELDS:
                if field in self.fields:
                    self.fields[field].disabled = True

    def clean_year(self):
        """Validate the minimum allowed year.

        Returns:
            int: Validated year.

        Raises:
            ValidationError: When the year is below the minimum.
        """
        year = self.cleaned_data["year"]
        if year < 1895:
            raise forms.ValidationError(ERROR_MOVIE_YEAR_MIN)
        return year

    def clean_price(self):
        """Validate the movie price is non-negative.

        Returns:
            Decimal: Validated price.

        Raises:
            ValidationError: When the price is negative.
        """
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError(ERROR_MOVIE_PRICE_NEGATIVE)
        return price
