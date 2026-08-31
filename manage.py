#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

# Add a directory in which Django will look up for models
sys.path.append(os.path.join(Path(__file__).resolve().parent, "models"))
# "common" es un junction a reciplus-common/django — se agrega directo al sys.path (no
# como paquete "common.X") para que hsl_7/user/shared se importen bare, igual en donde
# se generan las migraciones (el migrator) y en donde se consumen (aquí).
sys.path.append(os.path.join(Path(__file__).resolve().parent, "common"))


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
