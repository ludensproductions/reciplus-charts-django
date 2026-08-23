from django.template.loader import render_to_string
from django_eventstream import send_event

from apps.activity_feed.consts import (
    ACTIVITY_FEED_CHANNEL,
    ACTIVITY_FEED_EVENT_TYPE,
    ACTIVITY_ITEM_TEMPLATE,
)


def emit_activity(message: str):
    """Render an activity item for the given message and emit it to the activity feed.

    The message is rendered using the ``ACTIVITY_ITEM_TEMPLATE`` template and then
    sent as an event on the ``ACTIVITY_FEED_CHANNEL`` via ``send_event``.

    Args:
        message (str): Text content to include in the activity item.
    """
    html = render_to_string(
        template_name=ACTIVITY_ITEM_TEMPLATE,
        context={"message": message},
    )

    send_event(
        channel=ACTIVITY_FEED_CHANNEL,
        event_type=ACTIVITY_FEED_EVENT_TYPE,
        data=html,
        json_encode=False,  # No estamos mandando un JSON
    )
