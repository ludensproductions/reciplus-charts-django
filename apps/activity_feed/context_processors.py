from .consts import (
    EMIT_ACTIVITY_URL,
)


def activity_feed_constants(request):
    """Methods that provides some activity feed constants for the front to use.

    Args:
        request (HttpRequest): Incoming HTTP request that caused the
            exception.

    Returns:
        dict: Dictionary containing some activity feed constants.
    """
    return {
        "EMIT_ACTIVITY_URL": EMIT_ACTIVITY_URL,
    }
