from django.contrib.postgres.fields import DateRangeField
from django.core.validators import MinValueValidator
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractModel
from apps.reservations.consts import (
    MODEL_BOOKING_RANGE_LABEL,
    MODEL_CANCEL_END_LABEL,
    MODEL_CANCEL_START_LABEL,
    MODEL_CANCEL_TIME_LABEL,
    MODEL_EXTRA_FEE_LABEL,
    MODEL_GUEST_LABEL,
    MODEL_PROMOTION_POINTS_LABEL,
    MODEL_RESERVATION_TYPE_LABEL,
    MODEL_RESERVATION_VERBOSE_NAME,
    MODEL_RESERVATION_VERBOSE_NAME_PLURAL,
    MODEL_SCHEDULED_ARRIVE_LABEL,
    ReservationTypes,
)


class Reservation(AbstractModel):
    """Represents a reservation with booking and cancellation windows.

    This model stores guest metadata, arrival planning, reservation type,
    cancellation constraints, and optional commercial adjustments.

    Side Effects:
        Persists reservation records with soft-delete semantics for recovery
        and audit use cases.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    guest = models.CharField(max_length=100, verbose_name=MODEL_GUEST_LABEL)
    scheduled_arrive = models.DateTimeField(verbose_name=MODEL_SCHEDULED_ARRIVE_LABEL)
    reservation_type = models.CharField(choices=ReservationTypes, verbose_name=MODEL_RESERVATION_TYPE_LABEL)
    extra_fee = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0.0,
        validators=[
            MinValueValidator(limit_value=0),
        ],
        verbose_name=MODEL_EXTRA_FEE_LABEL,
    )
    promotion_points = models.PositiveIntegerField(default=0, verbose_name=MODEL_PROMOTION_POINTS_LABEL)

    # First date range: booking period.
    booking_range = DateRangeField(verbose_name=MODEL_BOOKING_RANGE_LABEL)

    # Second date range: cancellation period.
    cancel_start = models.DateField(verbose_name=MODEL_CANCEL_START_LABEL)
    cancel_end = models.DateField(verbose_name=MODEL_CANCEL_END_LABEL)
    cancel_time = models.TimeField(verbose_name=MODEL_CANCEL_TIME_LABEL)

    class Meta:
        """Django model metadata for storage and admin presentation."""

        db_table = "reservations"
        verbose_name = MODEL_RESERVATION_VERBOSE_NAME
        verbose_name_plural = MODEL_RESERVATION_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return a human-readable reservation identifier.

        Returns:
            str: Guest name associated with the reservation.
        """
        return f"{self.guest}"
