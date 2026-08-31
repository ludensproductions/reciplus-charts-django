import os
import sys
from pathlib import Path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
# "common" es un junction a reciplus-common/django — mismo sys.path.append que manage.py,
# necesario aquí también porque en prod se sirve vía asgi.py (daphne), no manage.py.
sys.path.append(os.path.join(BASE_DIR, "common"))

from apps.chat.websocket.routing import websocket_urlpatterns  # noqa: E402

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
