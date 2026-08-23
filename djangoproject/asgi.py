import os
from pathlib import Path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

from apps.chat.websocket.routing import websocket_urlpatterns

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(  # Requires the Origin header
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
