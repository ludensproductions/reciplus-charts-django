from django.db import models
from safedelete.models import SOFT_DELETE

from apps.comun.models import AbstractModel
from apps.genres.models import Genre
from apps.sales.models import Sale

from .consts import (
    FIELD_GENRE_LABEL,
    FIELD_MOVIE_LABEL,
    FIELD_PLOT_LABEL,
    FIELD_PRICE_LABEL,
    FIELD_QUANTITY_LABEL,
    FIELD_SALE_LABEL,
    FIELD_TITLE_LABEL,
    FIELD_YEAR_LABEL,
    MODEL_MOVIE_SALES_VERBOSE_NAME,
    MODEL_MOVIE_SALES_VERBOSE_NAME_PLURAL,
    MODEL_MOVIE_VERBOSE_NAME,
    MODEL_MOVIE_VERBOSE_NAME_PLURAL,
)


class Movie(AbstractModel):
    """Represent a movie with genre, pricing, and sales relations.

    This model stores core movie data used for catalog and sales operations.
    """

    _safedelete_policy = SOFT_DELETE
    title = models.CharField(FIELD_TITLE_LABEL, max_length=100)
    year = models.IntegerField(FIELD_YEAR_LABEL)
    genre = models.ForeignKey(
        Genre,
        verbose_name=FIELD_GENRE_LABEL,
        on_delete=models.CASCADE,
        related_name="movies",
        related_query_name="movie",
    )
    price = models.DecimalField(FIELD_PRICE_LABEL, max_digits=10, decimal_places=2)
    plot = models.TextField(FIELD_PLOT_LABEL)

    @property
    def sales_count(self):
        """Return the number of sales linked to this movie.

        Returns:
            int: Count of related sales.
        """
        return self.movie_sales.count()

    # These relations will be deleted when the movie is deleted.
    delete_on_cascade = [
        "movie_sale",  # Related SaleMovie objects
        "movie_sale__sale",  # Related Sale objects through SaleMovie
    ]

    # This list prevent to restore the sale if it has related objects
    parent_relations = [("géneros", "genre", "genres:index")]

    # This list prevent to delete the sale if it has related objects
    child_relations = [("Venta", "movie_sale__sale", "sales:index")]

    class Meta:
        db_table = "movies"
        verbose_name = MODEL_MOVIE_VERBOSE_NAME
        verbose_name_plural = MODEL_MOVIE_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return a display string for the movie.

        Returns:
            str: Movie year and title.
        """
        return f"{self.year} - {self.title}"


class MovieSales(AbstractModel):
    """Link sales to movies with quantities.

    This model represents a movie line item inside a sale.
    """

    _safedelete_policy = SOFT_DELETE

    sale = models.ForeignKey(
        Sale,
        verbose_name=FIELD_SALE_LABEL,
        related_query_name="movie_sale",
        related_name="movie_sales",
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(
        "Movie",
        verbose_name=FIELD_MOVIE_LABEL,
        on_delete=models.CASCADE,
        related_query_name="movie_sale",
        related_name="movie_sales",
    )
    quantity = models.PositiveIntegerField(FIELD_QUANTITY_LABEL)

    class Meta:
        db_table = "movie_sales"
        verbose_name = MODEL_MOVIE_SALES_VERBOSE_NAME
        verbose_name_plural = MODEL_MOVIE_SALES_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return the related sale as a string.

        Returns:
            str: Sale representation.
        """
        return f"{self.sale}"
