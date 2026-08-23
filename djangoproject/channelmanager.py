import re
from typing import Optional, Union

from django.contrib.auth.models import AnonymousUser
from django_eventstream.channelmanager import DefaultChannelManager

from apps.notification.consts import (
    NOTIFICATIONS_CHANNEL_PREFIX,
    NOTIFICATIONS_CHANNEL_REGEX,
)
from apps.users.models import User


class AuthenticationChannelManager(DefaultChannelManager):
    """Channel authorization manager.

    Channel authorization manager responsible for controlling read access
    to Server-Sent Events (SSE) channels based on authentication and
    ownership rules.

    This manager enforces:
    - Authentication and active-user requirements for all channels.
    - User ownership validation for per-user notification channels.
    - Explicit allow-listing of public or shared channels.

    Channels not explicitly authorized are denied by default.

    This class is intended to prevent:
    - Anonymous access to private SSE channels.
    - Cross-user access to notification streams.
    - Accidental exposure of sensitive real-time events.
    """

    def can_read_channel(self, user: Optional[Union[User, AnonymousUser]], channel: str):
        """Determines whether a user is allowed to read from a given SSE channel.

        Authorization rules:
        - The user must exist, be authenticated, and be active.
        - Notification channels require additional ownership checks.
        - Explicitly allow-listed channels may be accessible to all
          authenticated users.
        - All other channels are denied by default.

        Args:
            user (Optional[Union[User, AnonymousUser]]): User attempting
                to subscribe to the channel.
            channel (str): Name of the SSE channel being requested.

        Returns:
            bool: True if the user is authorized to read from the channel;
                False otherwise.
        """
        if not user or user.is_anonymous or not user.is_authenticated or not user.is_active:
            return False

        # Require auth for notifications channels
        if channel.startswith(NOTIFICATIONS_CHANNEL_PREFIX):
            return self.handle_notifications_channels_auth(
                user=user,
                channel=channel,
            )

        if channel == "activity-feed":
            return True

        return False

    def handle_notifications_channels_auth(self, user: Optional[Union[User, AnonymousUser]], channel: str) -> bool:
        """Validates access to per-user notification channels.

        Notification channels are expected to include the user's ID in
        the channel name. Access is granted only if the ID embedded in
        the channel matches the authenticated user's ID.

        This prevents users from subscribing to notification channels
        belonging to other users.

        Args:
            user (Optional[Union[User, AnonymousUser]]): Authenticated
                user attempting to access the channel.
            channel (str): Notification channel name containing the
                target user ID.

        Returns:
            bool: True if the user is authorized to read from the
                notification channel; False otherwise.
        """
        user_notifications_match = re.match(NOTIFICATIONS_CHANNEL_REGEX, channel)
        if not user_notifications_match:
            return False

        user_id_str = user_notifications_match.group(1)

        if not user_id_str:
            return False

        user_id = int(user_id_str)
        return user.id == user_id
