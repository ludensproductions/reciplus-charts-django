from django.core.validators import FileExtensionValidator
from django.db import models

from apps.comun.models import AbstractModel
from apps.comun.validators import (
    FileSizeValidator,
    curp_format_validator,
    strict_rfc_validator,
)

from .consts import (
    FIELD_BILLING_FILE_LABEL,
    FIELD_EMAIL_LABEL,
    FIELD_JUSTIFICATION_LABEL,
    FIELD_MODIFICATION_DATE_LABEL,
    FIELD_MOVIE_COVER_LABEL,
    FIELD_MOVIE_LABEL,
    FIELD_PASSWORD_LABEL,
    FIELD_PHONE_LABEL,
    FIELD_PRODUCTOR_LABEL,
    FIELD_QUANTITY_LABEL,
    FIELD_REGISTRATION_DATE_LABEL,
    MODEL_MOVIE_INVENTORY_VERBOSE_NAME,
    MODEL_MOVIE_INVENTORY_VERBOSE_NAME_PLURAL,
)


class MovieInventory(AbstractModel):
    """Store movie inventory stock and associated metadata.

    This model tracks quantities, producer details, and supporting documents
    used for compliance and inventory auditing.
    """

    movie = models.ForeignKey(
        "movies.Movie",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=FIELD_MOVIE_LABEL,
    )
    productor = models.CharField(max_length=255, null=False, blank=False, verbose_name=FIELD_PRODUCTOR_LABEL)
    quantity = models.IntegerField(verbose_name=FIELD_QUANTITY_LABEL)
    email = models.EmailField(max_length=255, null=False, blank=False, verbose_name=FIELD_EMAIL_LABEL)
    password = models.CharField(max_length=20, null=False, blank=False, verbose_name=FIELD_PASSWORD_LABEL)
    registration_date = models.DateField(verbose_name=FIELD_REGISTRATION_DATE_LABEL)
    modification_date = models.DateField(null=True, blank=True, verbose_name=FIELD_MODIFICATION_DATE_LABEL)
    phone = models.CharField(max_length=15, verbose_name=FIELD_PHONE_LABEL)
    billing_file = models.FileField(
        upload_to="billing",
        validators=[
            FileSizeValidator(max_mb=10),
            FileExtensionValidator(allowed_extensions=["pdf", "zip"]),
        ],
        verbose_name=FIELD_BILLING_FILE_LABEL,
    )
    curp = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        validators=[
            curp_format_validator,
        ],
    )
    rfc = models.CharField(
        max_length=100,
        validators=[
            # rfc_format_validator,
            strict_rfc_validator,
        ],
    )
    movie_cover = models.ImageField(upload_to="covers", verbose_name=FIELD_MOVIE_COVER_LABEL)
    justification = models.TextField(max_length=2000, null=False, blank=False, verbose_name=FIELD_JUSTIFICATION_LABEL)

    class Meta:
        db_table = "movies_inventory"
        verbose_name = MODEL_MOVIE_INVENTORY_VERBOSE_NAME
        verbose_name_plural = MODEL_MOVIE_INVENTORY_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    @property
    def movie_title(self):
        """Return the related movie title.

        Returns:
            str: Movie title.
        """
        return self.movie.title

    def __str__(self):
        """Return the string representation of the inventory record.

        Returns:
            str: Movie title.
        """
        return self.movie.title
