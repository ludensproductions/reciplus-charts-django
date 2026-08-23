from typing import Iterable

from django.template.loader import render_to_string
from django_eventstream import send_event

from apps.users.models import User

from .consts import (
    NOTIFICATION_STYLES,
    NOTIFICATIONS_CARD_TEMPLATE,
    NOTIFICATIONS_CHANNEL_PREFIX,
    NotificationTypes,
)
from .models import Notification


def get_notification_context(notification: Notification) -> dict:
    """Build the context dictionary for the notification template.

    Args:
        notification (Notification): Notification instance used to populate the template.

    Returns:
        dict: The notification data for the template.
    """
    return {
        "notification": notification,
        "notification_styles": NotificationUtils.get_notification_style(notification.notification_type),
    }


def render_notification(notification: Notification) -> str:
    """Render the notification template for a notification.

    Args:
        notification (Notification): Notification instance to render.

    Returns:
        str: The rendered template as a string.
    """
    context = get_notification_context(notification=notification)
    rendered_string = render_to_string(NOTIFICATIONS_CARD_TEMPLATE, context)
    rendered_string = rendered_string.strip().replace("\n", "")

    return rendered_string


def broadcast_notification(user, notification: Notification):
    """Broadcast a newly created notification to a user.

    Args:
        user (User): Target user receiving the notification.
        notification (Notification): Notification to broadcast.
    """
    unread_count = Notification.objects.filter(
        user=user,
        is_read=False,
        deleted__isnull=True,
    ).count()
    rendered_string = render_notification(notification=notification)

    send_event(
        f"{NOTIFICATIONS_CHANNEL_PREFIX}{user.pk}",
        "message",
        {"count": unread_count, "notification_html": str(rendered_string)},
    )


class NotificationUtils:
    """Class that provides utility functions to create notifications quickly."""

    @staticmethod
    def create_notification(
        user: User, title: str, content: str, notification_type=NotificationTypes.DEFAULT
    ) -> Notification:
        """Create a new notification for a user.

        Args:
            user (User): User instance.
            title (str): Notification title.
            content (str): Notification message string.
            notification_type (NotificationTypes): NotificationTypes choice.

        Returns:
            Notification: Created notification instance.
        """
        notification = Notification.objects.create(
            user=user,
            title=title,
            content=content,
            notification_type=notification_type,  # Can pass enum directly!
        )
        return notification

    @staticmethod
    def create_notification_multiple_users(
        users: Iterable[User], title: str, content: str, notification_type=NotificationTypes.DEFAULT
    ) -> Iterable[Notification]:
        """Create a new notification for multiple users.

        Args:
            users (Iterable[User]): An iterable of users.
            title (str): Notification title.
            content (str): Notification message string.
            notification_type (NotificationTypes): NotificationTypes choice.

        Returns:
            Iterable[Notification]: Created notification instances.
        """
        new_notifications = []
        for user in users:
            new_notification = NotificationUtils.create_notification(
                user=user,
                title=title,
                content=content,
                notification_type=notification_type,
            )
            new_notifications.append(new_notification)

        return new_notifications

    @staticmethod
    def create_urgent_notification(user: User, title: str, content: str) -> Notification:
        """Shortcut to create an urgent notification.

        Args:
            user (User): User instance.
            title (str): Notification title.
            content (str): Notification message string.

        Returns:
            Notification: Created notification instance.
        """
        return NotificationUtils.create_notification(user, title, content, NotificationTypes.URGENT)

    @staticmethod
    def create_success_notification(user: User, title: str, content: str) -> Notification:
        """Shortcut to create success notification.

        Args:
            user (User): User instance.
            title (str): Notification title.
            content (str): Notification message string.

        Returns:
            Notification: Created notification instance.
        """
        return NotificationUtils.create_notification(user, title, content, NotificationTypes.SUCCESS)

    @staticmethod
    def create_error_notification(user: User, title: str, content: str) -> Notification:
        """Shortcut to create an error notification.

        Args:
            user (User): User instance.
            title (str): Notification title.
            content (str): Notification message string.

        Returns:
            Notification: Created notification instance.
        """
        return NotificationUtils.create_notification(user, title, content, NotificationTypes.ERROR)

    @staticmethod
    def create_info_notification(user: User, title: str, content: str) -> Notification:
        """Shortcut to create an info notification.

        Args:
            user (User): User instance.
            title (str): Notification title.
            content (str): Notification message string.

        Returns:
            Notification: Created notification instance.
        """
        return NotificationUtils.create_notification(user, title, content, NotificationTypes.INFO)

    @staticmethod
    def create_urgent_notifications(users: Iterable[User], title: str, content: str) -> Iterable[Notification]:
        """Shortcut to create urgent notifications.

        Args:
            users (Iterable[User]): An iterable of users.
            title (str): Notification title.
            content (str): Notification message string.

        Returns:
            Iterable[Notification]: Created notification instances.
        """
        return NotificationUtils.create_notification_multiple_users(users, title, content, NotificationTypes.URGENT)

    @staticmethod
    def create_success_notifications(users: Iterable[User], title: str, content: str) -> Iterable[Notification]:
        """Shortcut to create success notifications.

        Args:
            users (Iterable[User]): An iterable of users.
            title (str): Notification title.
            content (str): Notification message string.

        Returns:
            Iterable[Notification]: Created notification instances.
        """
        return NotificationUtils.create_notification_multiple_users(users, title, content, NotificationTypes.SUCCESS)

    @staticmethod
    def create_error_notifications(users: Iterable[User], title: str, content: str) -> Iterable[Notification]:
        """Shortcut to create error notifications.

        Args:
            users (Iterable[User]): An iterable of users.
            title (str): Notification title.
            content (str): Notification message string.

        Returns:
            Iterable[Notification]: Created notification instances.
        """
        return NotificationUtils.create_notification_multiple_users(users, title, content, NotificationTypes.ERROR)

    @staticmethod
    def create_info_notifications(users: Iterable[User], title: str, content: str) -> Iterable[Notification]:
        """Shortcut to create info notifications.

        Args:
            users (Iterable[User]): An iterable of users.
            title (str): Notification title.
            content (str): Notification message string.

        Returns:
            Iterable[Notification]: Created notification instances.
        """
        return NotificationUtils.create_notification_multiple_users(users, title, content, NotificationTypes.INFO)

    @staticmethod
    def get_notification_style(notification_type):
        """Get styling information for a notification type.

        Args:
            notification_type (NotificationTypes): NotificationTypes choice.

        Returns:
            dict: Styling information for the provided type.
        """
        return NOTIFICATION_STYLES.get(notification_type, NOTIFICATION_STYLES[NotificationTypes.DEFAULT])
