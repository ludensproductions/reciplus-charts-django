from typing import List

from ninja import Field, Schema
from pydantic import ConfigDict

from apps.notification.consts import (
    COUNT_DESCRIPTION,
    HAS_NEXT_DESCRIPTION,
    NEW_NOTIFICATION_IDS_DESCRIPTION,
    NOTIFICATIONS_HTML_DESCRIPTION,
    PAGE_DESCRIPTION,
)


class ReadNotificationIn(Schema):  # noqa
    model_config = ConfigDict(extra="forbid")

    page: int = Field(..., description=PAGE_DESCRIPTION)
    new_notification_ids: List[int] = Field(..., description=NEW_NOTIFICATION_IDS_DESCRIPTION)


class ReadNotificationOut(Schema):  # noqa
    model_config = ConfigDict(extra="forbid")

    notifications_html: List[str] = Field(..., description=NOTIFICATIONS_HTML_DESCRIPTION)
    has_next: bool = Field(..., description=HAS_NEXT_DESCRIPTION)
    count: int = Field(..., description=COUNT_DESCRIPTION)
