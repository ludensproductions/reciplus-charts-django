import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")

application = get_wsgi_application()
