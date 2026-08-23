from django.db.models import TextChoices

MESSAGE_TEMPLATE = "chat/_message.html"


class MessageTypes(TextChoices):
    """Class that contains all message types for the ChatConsumer."""

    CHAT_MESSAGE = "chat.message"
