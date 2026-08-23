from django_q.tasks import async_task

from apps.notification.utils import NotificationUtils


class SuccessNotificationMixin:
    """Mixin to create success notifications after a form is successfully submitted.

    This mixin requires three attributes to be defined in the view:
    - `notification_message`: A string that can be formatted with the cleaned data from the form. This message will be used as the content of the notification.
    - `notification_title`: A string that will be used as the title of the notification.
    - `notification_users`: An iterable of User objects that will receive the notification. If this attribute is not set, the notification will be sent to the user who submitted the form (i.e., `self.request.user`).
    """

    def form_valid(self, form):  # noqa: D102
        response = super().form_valid(form)

        notification_message = self.get_notification_message(form.cleaned_data)
        notification_title = self.get_notification_title()
        notification_users = self.get_notification_users_queryset()

        if notification_message and notification_title and notification_users:
            async_task(
                NotificationUtils.create_success_notifications,
                notification_users,
                notification_title,
                notification_message,
            )
        return response

    def get_notification_message(self, cleaned_data: dict | None) -> str:
        """Generate the notification message based on the cleaned data from the form. If cleaned_data is None, return the default notification message.

        Args:
            cleaned_data (dict | None): The cleaned data from the form, which can be used to format the notification message. If None, the default message will be returned.

        Returns:
            str: The notification message.
        """
        if not cleaned_data:
            return getattr(self, "notification_message", "")

        return getattr(self, "notification_message", "") % cleaned_data

    def get_notification_title(self):
        """Get the notification title. By default, it returns the value of `self.notification_title`, but it can be overridden to provide dynamic titles based on the context.

        Returns:
            str: The notification title.
        """
        return getattr(self, "notification_title", "")

    def get_notification_users_queryset(self):
        """Get the queryset of users to receive the notification. By default, it returns `self.notification_users` if it's set, or `[self.request.user]` if `self.notification_users` is not set and `self.request` is available. If neither condition is met, it returns an empty list.

        Returns:
            Iterable[User]: The queryset of users to receive the notification.
        """
        if not getattr(self, "notification_users", None) and hasattr(self, "request"):
            return [self.request.user]

        if not getattr(self, "notification_users", None) and not hasattr(self, "request"):
            return []

        return getattr(self, "notification_users", None)
