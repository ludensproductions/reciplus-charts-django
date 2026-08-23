from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractModel
from apps.event_planner import consts as event_planner_consts


class Event(AbstractModel):
    """Group activities and attendees within a single event.

    This model represents a scheduled event with a title, start date, and
    optional responsible user. Related activities and attendees are stored in
    separate models linked to this event.

    Attributes:
        title (str): Event title.
        date_start (date): Event start date.
        location (str): Event location.
        responsible (User | None): Responsible user, if assigned.
        folio (str | None): Optional event folio identifier.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    title = models.CharField(event_planner_consts.EVENT_TITLE_LABEL, max_length=200)
    date_start = models.DateField(event_planner_consts.EVENT_DATE_START_LABEL)
    location = models.CharField(event_planner_consts.EVENT_LOCATION_LABEL, max_length=200)
    responsible = models.ForeignKey(
        "users.User",
        related_name="events",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=event_planner_consts.EVENT_RESPONSIBLE_LABEL,
    )
    folio = models.CharField(
        event_planner_consts.EVENT_FOLIO_LABEL,
        max_length=100,
        null=True,
        blank=True,
    )
    # delete_on_cascade = [
    #     "event_activities",
    # ]

    class Meta:
        db_table = "events"
        verbose_name = event_planner_consts.EVENT_VERBOSE_NAME
        verbose_name_plural = event_planner_consts.EVENT_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return a display string for the event.

        Returns:
            str: Event title and start date.
        """
        return event_planner_consts.EVENT_DISPLAY.format(title=self.title, date=self.date_start)

    @property
    def get_responsible_name(self):
        """Return the responsible user's name for display.

        Returns:
            str: Responsible name or a not-available placeholder.
        """
        if self.responsible:
            return event_planner_consts.RESPONSIBLE_DISPLAY_PIPE.format(
                first_name=self.responsible.first_name,
                last_name=self.responsible.last_name,
            )
        return event_planner_consts.VALUE_NOT_AVAILABLE

    @property
    def get_responsible_name_index(self):
        """Return the responsible user's name in index format.

        Returns:
            str: Responsible name or a not-available placeholder.
        """
        if self.responsible:
            return event_planner_consts.RESPONSIBLE_DISPLAY_COMMA.format(
                first_name=self.responsible.first_name,
                last_name=self.responsible.last_name,
            )
        return event_planner_consts.VALUE_NOT_AVAILABLE

    @property
    def get_index_activities(self):
        """Return a summary of event activities for listing.

        Returns:
            str: Joined activity summary or a not-available placeholder.
        """
        event_activities = self.event_activities.filter(deleted__isnull=True)

        if not event_activities.exists():
            return event_planner_consts.VALUE_NOT_AVAILABLE

        return event_planner_consts.EVENT_ACTIVITIES_JOINER.join(
            [
                event_planner_consts.EVENT_ACTIVITY_INDEX_ITEM.format(
                    activity=ea.activity.name,
                    location=ea.activity.location,
                )
                for ea in event_activities
            ]
        )


class EventActivity(AbstractModel):
    """Link an event to one of its activities.

    This model stores the relationship between an event and an activity,
    including optional capacity and tracking code.

    Attributes:
        event (Event): Parent event.
        activity (Activity): Linked activity.
        capacity (int | None): Optional capacity for the activity.
        code (str | None): Optional tracking code.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    event = models.ForeignKey(
        Event,
        related_name="event_activities",
        related_query_name="event_activity",
        on_delete=models.CASCADE,
        verbose_name=event_planner_consts.EVENT_VERBOSE_NAME,
    )
    activity = models.ForeignKey(
        "activities.Activity",
        related_name="activity_events",
        on_delete=models.CASCADE,
        verbose_name=event_planner_consts.EVENT_ACTIVITY_LABEL,
    )
    capacity = models.PositiveIntegerField(
        event_planner_consts.EVENT_ACTIVITY_CAPACITY_LABEL,
        null=True,
        blank=True,
    )
    code = models.CharField(
        event_planner_consts.EVENT_ACTIVITY_CODE_LABEL,
        max_length=50,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "event_activities"
        verbose_name = event_planner_consts.EVENT_ACTIVITY_VERBOSE_NAME
        verbose_name_plural = event_planner_consts.EVENT_ACTIVITY_VERBOSE_NAME_PLURAL

    def __str__(self):
        """Return a display string for the event activity.

        Returns:
            str: Event and activity summary.
        """
        return event_planner_consts.EVENT_ACTIVITY_DISPLAY.format(
            event=self.event.title,
            activity=self.activity.name,
            capacity=self.capacity,
        )


class EventAttendee(AbstractModel):
    """Store an attendee record for an event.

    Attributes:
        event (Event): Parent event.
        full_name (str): Attendee full name.
        email (str): Attendee email address.
        phone (str): Attendee phone number.
        notes (str): Optional notes about the attendee.
    """

    event = models.ForeignKey(
        Event,
        related_name="attendees",
        on_delete=models.CASCADE,
        verbose_name=event_planner_consts.EVENT_VERBOSE_NAME,
    )
    full_name = models.CharField(event_planner_consts.ATTENDEE_FULL_NAME_LABEL, max_length=200)
    email = models.EmailField(event_planner_consts.ATTENDEE_EMAIL_LABEL)
    phone = models.CharField(event_planner_consts.ATTENDEE_PHONE_LABEL, max_length=50, blank=True)
    notes = models.TextField(event_planner_consts.ATTENDEE_NOTES_LABEL, blank=True)

    class Meta:
        db_table = "event_attendees"
        verbose_name = event_planner_consts.EVENT_ATTENDEE_VERBOSE_NAME
        verbose_name_plural = event_planner_consts.EVENT_ATTENDEE_VERBOSE_NAME_PLURAL

    def __str__(self):
        """Return a display string for the attendee.

        Returns:
            str: Attendee name and email.
        """
        return f"{self.full_name} - {self.email}"
