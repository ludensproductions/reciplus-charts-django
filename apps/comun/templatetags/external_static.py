import json
from functools import lru_cache
from pathlib import Path

from django import template
from django.conf import settings
from django.templatetags.static import static

from apps.comun.static_assets import EXTERNAL_ASSET_ROOT, normalize_external_asset_url

register = template.Library()


@lru_cache(maxsize=1)
def _load_manifest():
    static_root = getattr(settings, "STATIC_ROOT", "")
    if not static_root:
        return {}

    manifest_path = Path(static_root) / EXTERNAL_ASSET_ROOT / "manifest.json"
    if not manifest_path.exists():
        return {}

    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


@register.simple_tag
def external_static_url(url):
    """Return a local static URL for a downloaded external asset when available."""
    normalized_url = normalize_external_asset_url(url)
    relative_path = _load_manifest().get(normalized_url)
    if relative_path:
        return static(relative_path)
    return url
