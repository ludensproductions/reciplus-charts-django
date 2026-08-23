from .consts import (
    GET_NOTIFICATIONS_URL,
    NOTIFICATIONS_CHANNEL_PREFIX,
)


def notifications(request):
    """Methods that provides some notification constants for the front to use.

    Args:
        request (HttpRequest): Incoming HTTP request that caused the
            exception.

    Returns:
        dict: Dictionary containing some notification constants.
    """
    return {
        "NOTIFICATIONS_CHANNEL_PREFIX": NOTIFICATIONS_CHANNEL_PREFIX,
        "GET_NOTIFICATIONS_URL": GET_NOTIFICATIONS_URL,
    }
