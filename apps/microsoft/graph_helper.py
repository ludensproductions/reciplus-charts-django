import requests
from django.conf import settings

from apps.microsoft.consts import USER_ME_ENDPOINT


def get_user(token):
    """Docstring for get_user."""
    user = requests.get(
        f"{settings.MICROSOFT_GRAPH_API_URL}{USER_ME_ENDPOINT}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return user.json()
