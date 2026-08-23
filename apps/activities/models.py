from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractModel

from .consts import ACTIVITY_TYPE_CONFERENCE, ACTIVITY_TYPE_WEBINAR, ACTIVITY_TYPE_WORKSHOP


class Activity(AbstractModel):
    """Model representing an activity with name, location, and type.

    Activities can be workshops, conferences, or webinars, and use soft delete.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(_("Name"), max_length=150)
    location = models.CharField(_("Location"), max_length=150)
    activity_type = models.CharField(
        _("Type"),
        max_length=50,
        choices=[
            ("CONFERENCE", ACTIVITY_TYPE_CONFERENCE),
            ("WEBINAR", ACTIVITY_TYPE_WEBINAR),
            ("WORKSHOP", ACTIVITY_TYPE_WORKSHOP),
        ],
        default="WORKSHOP",
    )

    class Meta:
        """Meta configuration for Activity model."""

        db_table = "activities"
        verbose_name = _("Actividad")
        verbose_name_plural = _("Actividades")
        ordering = ["name"]

    def __str__(self):
        """Return string representation of Activity with name and location."""
        return f"{self.name} ({self.location})"
