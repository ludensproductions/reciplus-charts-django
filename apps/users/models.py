from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import DO_NOTHING, Q
from safedelete.models import SOFT_DELETE, SOFT_DELETE_CASCADE

from apps.comun.models import AbstractNullableModel, AbstrasModelNoUser
from apps.departments.models import Departamento
from apps.discord.managers import SafeUserOAuth2Manager
from apps.groups.models import CustomGroup
from apps.positions.models import Puesto

from .consts import (
    FIELD_ADDRESS_LABEL,
    FIELD_CALLE_LABEL,
    FIELD_CITY_LABEL,
    FIELD_CLAVE_LABEL,
    FIELD_CODIGO_POSTAL_LABEL,
    FIELD_COLONIA_LABEL,
    FIELD_COUNTRY_LABEL,
    FIELD_DARK_MODE_LABEL,
    FIELD_DEPARTAMENTO_LABEL,
    FIELD_DOMICILIO_LABEL,
    FIELD_EMAIL_LABEL,
    FIELD_ESTADO_LABEL,
    FIELD_FIRST_NAME_LABEL,
    FIELD_GRUPO_LABEL,
    FIELD_IMAGE_LABEL,
    FIELD_LAST_NAME_LABEL,
    FIELD_MOBILE_PHONE_LABEL,
    FIELD_MUNICIPIO_LABEL,
    FIELD_NUMERO_EXTERIOR_LABEL,
    FIELD_NUMERO_INTERIOR_LABEL,
    FIELD_PAIS_LABEL,
    FIELD_PUESTO_LABEL,
    FIELD_RESPONSIVA_FILE_LABEL,
    FIELD_SECOND_LAST_NAME_LABEL,
    FIELD_STATE_LABEL,
    FIELD_USER_LABEL,
    FIELD_WORK_PHONE_LABEL,
    MODEL_CODIGO_POSTAL_VERBOSE_NAME,
    MODEL_CODIGO_POSTAL_VERBOSE_NAME_PLURAL,
    MODEL_DOMICILIO_VERBOSE_NAME,
    MODEL_DOMICILIO_VERBOSE_NAME_PLURAL,
    MODEL_ESTADO_VERBOSE_NAME,
    MODEL_ESTADO_VERBOSE_NAME_PLURAL,
    MODEL_MUNICIPIO_VERBOSE_NAME,
    MODEL_MUNICIPIO_VERBOSE_NAME_PLURAL,
    MODEL_PAIS_VERBOSE_NAME,
    MODEL_PAIS_VERBOSE_NAME_PLURAL,
    MODEL_RESPONSIVA_VERBOSE_NAME,
    MODEL_RESPONSIVA_VERBOSE_NAME_PLURAL,
    MODEL_USER_GROUP_VERBOSE_NAME,
    MODEL_USER_GROUP_VERBOSE_NAME_PLURAL,
    MODEL_USER_VERBOSE_NAME,
    MODEL_USER_VERBOSE_NAME_PLURAL,
)


class User(AbstractUser, AbstractNullableModel):
    """Application user with extended profile, HR data, and preferences.

    This model extends Django's built-in user with additional fields used across
    the platform for profile data, organizational placement, and UI preferences.
    It is the canonical identity record for access control and personalization.

    Attributes:
        first_name: Given name.
        last_name: Primary family name.
        second_last_name: Secondary family name (optional).
        image: Profile image path (optional).
        departamento: Related department (optional).
        puesto: Related position (optional).
        telefono_trabajo: Work phone number (optional).
        celular: Mobile phone number (optional).
        city: City name (optional).
        state: State name (optional).
        country: Country name (optional).
        address: Street address (optional).
        dark_mode: Whether the user prefers dark mode.
        domicilio: Related address entity (optional).
        email: Email address.
        groups: Custom groups associated with the user.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    first_name = models.CharField(FIELD_FIRST_NAME_LABEL, max_length=255)
    last_name = models.CharField(FIELD_LAST_NAME_LABEL, max_length=255)
    second_last_name = models.CharField(FIELD_SECOND_LAST_NAME_LABEL, max_length=255, blank=True, null=True)
    image = models.ImageField(
        FIELD_IMAGE_LABEL,
        upload_to="profiles/",
        max_length=255,
        blank=True,
        null=True,
        default="/static/assets/img/avatars/blank-profile-pic.png",
    )
    departamento = models.ForeignKey(
        Departamento,
        verbose_name=FIELD_DEPARTAMENTO_LABEL,
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    puesto = models.ForeignKey(
        Puesto,
        verbose_name=FIELD_PUESTO_LABEL,
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    telefono_trabajo = models.CharField(FIELD_WORK_PHONE_LABEL, max_length=10, null=True, blank=True)
    celular = models.CharField(FIELD_MOBILE_PHONE_LABEL, max_length=10, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)

    city = models.CharField(FIELD_CITY_LABEL, max_length=255, blank=True, null=True)
    state = models.CharField(FIELD_STATE_LABEL, max_length=255, blank=True)
    country = models.CharField(FIELD_COUNTRY_LABEL, max_length=255, blank=True)
    address = models.CharField(FIELD_ADDRESS_LABEL, max_length=255, blank=True)
    dark_mode = models.BooleanField(FIELD_DARK_MODE_LABEL, default=False)
    domicilio = models.ForeignKey(
        "Domicilio",
        verbose_name=FIELD_DOMICILIO_LABEL,
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    email = models.EmailField(FIELD_EMAIL_LABEL, blank=False, null=False)
    is_banned = models.BooleanField(default=False)
    force_logout_at = models.DateTimeField(null=True, blank=True)
    microsoft_id = models.CharField(max_length=255, null=True, blank=True)
    discord_id = models.CharField(max_length=255, null=True, blank=True)
    discord_tag = models.CharField(max_length=255, null=True, blank=True)

    objects = SafeUserOAuth2Manager()
    groups = models.ManyToManyField(
        CustomGroup,
        through="UserGroup",
        through_fields=("user", "auth_group"),
        related_name="users",
    )

    class Meta:
        db_table = "users"
        verbose_name = MODEL_USER_VERBOSE_NAME
        verbose_name_plural = MODEL_USER_VERBOSE_NAME_PLURAL
        ordering = ["id"]
        permissions = [
            ("ban_user", "Can ban/unban user"),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["username"],
                condition=Q(deleted__isnull=True) & Q(username__isnull=False),
                name="unique_active_username",
            ),
            models.UniqueConstraint(
                fields=["microsoft_id"],
                condition=Q(deleted__isnull=True) & Q(microsoft_id__isnull=False),
                name="unique_active_microsoft_id",
            ),
            models.UniqueConstraint(
                fields=["discord_id"],
                condition=Q(deleted__isnull=True) & Q(discord_id__isnull=False),
                name="unique_active_discord_id",
            ),
        ]

    def __str__(self):
        """Return a human-readable display name.

        Concatenates the user's first and last name for display purposes.

        Returns:
            str: The user's full name (first name + last name).
        """
        return f"{self.first_name} {self.last_name}"


class Reponsiva(AbstractNullableModel):
    """Responsibility document associated with a user.

    This model stores the signed responsibility file for a given user.

    Attributes:
        user: Related user who owns the document.
        responsiva: File path for the responsibility document (optional).
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    user = models.ForeignKey(User, verbose_name=FIELD_USER_LABEL, related_name="+", on_delete=models.DO_NOTHING)
    responsiva = models.FileField(
        FIELD_RESPONSIVA_FILE_LABEL,
        upload_to="responsivas/",
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "responsiva"
        verbose_name = MODEL_RESPONSIVA_VERBOSE_NAME
        verbose_name_plural = MODEL_RESPONSIVA_VERBOSE_NAME_PLURAL
        ordering = ["id"]


class Pais(AbstractNullableModel):
    """Country catalog entry used for address normalization.

    This catalog powers address selection and ensures consistent country names.

    Attributes:
        pais: Country name.
        clave: Country code.
    """

    _safe_delete_policy = SOFT_DELETE_CASCADE
    pais = models.CharField(FIELD_PAIS_LABEL, max_length=255)
    clave = models.CharField(FIELD_CLAVE_LABEL, max_length=4)

    class Meta:
        verbose_name = MODEL_PAIS_VERBOSE_NAME
        verbose_name_plural = MODEL_PAIS_VERBOSE_NAME_PLURAL
        db_table = "pais"
        ordering = ["-id"]

    def __str__(self):
        """Return the country name.

        Returns:
            str: Country name.
        """
        return self.pais


class Estado(AbstractNullableModel):
    """State catalog entry linked to a country.

    This model provides standardized state values for addresses.

    Attributes:
        pais: Related country.
        estado: State name.
        clave: State code.
    """

    _safe_delete_policy = SOFT_DELETE_CASCADE
    pais = models.ForeignKey("Pais", verbose_name=FIELD_PAIS_LABEL, related_name="+", on_delete=DO_NOTHING)
    estado = models.CharField(FIELD_ESTADO_LABEL, max_length=255)
    clave = models.CharField(FIELD_CLAVE_LABEL, max_length=5)

    class Meta:
        verbose_name = MODEL_ESTADO_VERBOSE_NAME
        verbose_name_plural = MODEL_ESTADO_VERBOSE_NAME_PLURAL
        db_table = "estado"
        ordering = ["-id"]

    def __str__(self):
        """Return the state name.

        Returns:
            str: State name.
        """
        return self.estado


class Domicilio(AbstractNullableModel):
    """Address information linked to a municipality and postal code.

    This record captures structured address data for users.

    Attributes:
        municipio: Related municipality.
        colonia: Neighborhood name.
        codigo_postal: Related postal code.
        calle: Street name.
        numero_exterior: Exterior number.
        numero_interior: Interior number (optional).
    """

    _safe_delete_policy = SOFT_DELETE_CASCADE
    municipio = models.ForeignKey(
        "Municipio",
        verbose_name=FIELD_MUNICIPIO_LABEL,
        related_name="+",
        on_delete=DO_NOTHING,
    )
    colonia = models.CharField(FIELD_COLONIA_LABEL, max_length=255)
    codigo_postal = models.ForeignKey(
        "CodigoPostal",
        verbose_name=FIELD_CODIGO_POSTAL_LABEL,
        related_name="+",
        on_delete=DO_NOTHING,
    )
    calle = models.CharField(FIELD_CALLE_LABEL, max_length=100)
    numero_exterior = models.CharField(FIELD_NUMERO_EXTERIOR_LABEL, max_length=10)
    numero_interior = models.CharField(FIELD_NUMERO_INTERIOR_LABEL, max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = MODEL_DOMICILIO_VERBOSE_NAME
        verbose_name_plural = MODEL_DOMICILIO_VERBOSE_NAME_PLURAL
        db_table = "domicilio"
        ordering = ["-id"]


class Municipio(AbstractNullableModel):
    """Municipality catalog entry linked to a state.

    This catalog ensures consistent municipality values for addresses.

    Attributes:
        estado: Related state.
        municipio: Municipality name.
        clave: Municipality code.
    """

    _safe_delete_policy = SOFT_DELETE_CASCADE
    estado = models.ForeignKey("Estado", verbose_name=FIELD_ESTADO_LABEL, related_name="+", on_delete=DO_NOTHING)
    municipio = models.CharField(FIELD_MUNICIPIO_LABEL, max_length=255)
    clave = models.CharField(FIELD_CLAVE_LABEL, max_length=8)

    class Meta:
        verbose_name = MODEL_MUNICIPIO_VERBOSE_NAME
        verbose_name_plural = MODEL_MUNICIPIO_VERBOSE_NAME_PLURAL
        db_table = "municipio"
        ordering = ["-id"]

    def __str__(self):
        """Return the municipality name.

        Returns:
            str: Municipality name.
        """
        return self.municipio


class CodigoPostal(AbstractNullableModel):
    """Postal code catalog entry linked to a municipality.

    This catalog normalizes postal codes for address records.

    Attributes:
        municipio: Related municipality.
        codigo_postal: Postal code value.
    """

    _safe_delete_policy = SOFT_DELETE_CASCADE
    municipio = models.ForeignKey(
        "Municipio",
        verbose_name=FIELD_MUNICIPIO_LABEL,
        related_name="+",
        on_delete=DO_NOTHING,
    )
    codigo_postal = models.CharField(FIELD_CODIGO_POSTAL_LABEL, max_length=255)

    class Meta:
        verbose_name = MODEL_CODIGO_POSTAL_VERBOSE_NAME
        verbose_name_plural = MODEL_CODIGO_POSTAL_VERBOSE_NAME_PLURAL
        db_table = "codigo_postal"
        ordering = ["-id"]

    def __str__(self):
        """Return the postal code.

        Returns:
            str: Postal code value.
        """
        return str(self.codigo_postal)


class UserGroup(AbstrasModelNoUser):
    """Join model that associates users with custom groups.

    This model defines explicit user-to-group assignments for permissions.

    Attributes:
        auth_group: Related custom group.
        user: Related user.
    """

    _safe_delete_policy = SOFT_DELETE
    auth_group = models.ForeignKey(
        CustomGroup,
        verbose_name=FIELD_GRUPO_LABEL,
        related_name="group_user",
        related_query_name="groups_users",
        on_delete=models.DO_NOTHING,
    )
    user = models.ForeignKey(
        "User",
        verbose_name=FIELD_USER_LABEL,
        related_name="user_group",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = MODEL_USER_GROUP_VERBOSE_NAME
        verbose_name_plural = MODEL_USER_GROUP_VERBOSE_NAME_PLURAL
        db_table = "user_groups"
        ordering = ["-id"]
