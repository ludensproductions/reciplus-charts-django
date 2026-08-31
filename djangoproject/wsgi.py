import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
# "common" es un junction a reciplus-common/django — mismo sys.path.append que manage.py.
sys.path.append(os.path.join(BASE_DIR, "common"))
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")

application = get_wsgi_application()
