from django.conf import settings


def site_theme(request):
    """Returns the theme configured in settings.py or 'axxon' by default."""
    return {"SITE_THEME": getattr(settings, "SITE_THEME", "axxon")}
