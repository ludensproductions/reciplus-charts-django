from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification
from .utils import broadcast_notification


@receiver(post_save, sender=Notification)
def handle_new_notification(sender, instance, created, **kwargs):
    """Method to handle the broadcast in the creation of a Notification.

    Args:
        sender: (type[Notification]): The type (or the model) who sends the signal.
        instance (Notification): The new notiication instance.
        created (bool): Bool that represents if the instance is new.
        kwargs (dict): Keyword arguments sent by Django.
    """
    if created:
        broadcast_notification(instance.user, instance)
