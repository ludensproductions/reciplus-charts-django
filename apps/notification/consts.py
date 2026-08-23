from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

NOTIFICATIONS_CHANNEL_PREFIX = "user-notifications-"
NOTIFICATIONS_CHANNEL_REGEX = rf"^{NOTIFICATIONS_CHANNEL_PREFIX}(\d+)$"
NOTIFICATIONS_CARD_TEMPLATE = "notification/notification_card.html"
GET_NOTIFICATIONS_URL = "/api/notifications"


class NotificationTypes(TextChoices):
    """Enumeration of supported notification types.

    This class defines the allowed categorical types for notifications,
    typically used to:
    - Control visual presentation (colors, icons, emphasis).
    - Convey semantic meaning and urgency to the user.
    - Enforce consistency across the application.

    The values of this enumeration are stored in the database, while the
    human-readable labels are intended for display purposes.
    """

    URGENT = "urgent", _("Urgente")
    SUCCESS = "success", _("Éxito")
    INFO = "info", _("Información")
    ERROR = "alert", _("Error")
    DEFAULT = "default", _("Predeterminado")


NOTIFICATION_STYLES = {
    NotificationTypes.URGENT: {"css_class": "text-warning", "icon": "fa-exclamation-triangle"},
    NotificationTypes.SUCCESS: {"css_class": "text-success", "icon": "fa-check-circle"},
    NotificationTypes.INFO: {"css_class": "text-info", "icon": "fa-info-circle"},
    NotificationTypes.ERROR: {"css_class": "text-danger", "icon": "fa-times-circle"},
    NotificationTypes.DEFAULT: {"css_class": "text-secondary", "icon": "fa-user"},
}

# Schema Descriptions
PAGE_DESCRIPTION = _("Current notification page.")
NEW_NOTIFICATION_IDS_DESCRIPTION = _("New notifications IDs.")
NOTIFICATIONS_HTML_DESCRIPTION = _("List of notifications as HTMLs.")
HAS_NEXT_DESCRIPTION = _("Indicator that says if there are more notifications.")
COUNT_DESCRIPTION = _("Current count of notifications.")
