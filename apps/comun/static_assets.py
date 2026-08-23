import hashlib
import re
from pathlib import PurePosixPath
from urllib.parse import urljoin, urlparse

from apps.comun.consts import (
    CSS_ASSET_URL_REGEX,
    CSS_NESTED_ASSET_URL_REGEX,
    CSS_RELATIVE_URL_REGEX,
    DJANGO_EXTERNAL_STATIC_TAG_REGEX,
    EXTERNAL_ASSET_ROOT,
    HTML_ASSET_URL_REGEX,
    JS_IMPORT_URL_REGEX,
)

SUPPORTED_ASSET_TYPES = (
    "text/css",
    "application/css",
    "javascript",
    "ecmascript",
)

SUPPORTED_EMBEDDED_TYPES = (
    "font/",
    "application/font",
    "application/octet-stream",
    "image/",
)

CONTENT_TYPE_EXTENSION_MAP = {
    "css": ".css",
    "javascript": ".js",
    "ecmascript": ".js",
    "font": ".woff2",
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/svg": ".svg",
}


def normalize_external_asset_url(url: str) -> str:
    """Return a normalized absolute URL for external asset references."""
    if url.startswith("//"):
        return f"https:{url}"
    return url


def iter_external_asset_urls(content: str, suffix: str) -> list[str]:
    """Extract normalized external asset URLs from supported HTML, CSS, and JS sources."""
    lowered_suffix = suffix.lower()
    if lowered_suffix in {".html", ".htm"}:
        matches = HTML_ASSET_URL_REGEX.findall(content) + DJANGO_EXTERNAL_STATIC_TAG_REGEX.findall(content)
    elif lowered_suffix == ".css":
        matches = CSS_ASSET_URL_REGEX.findall(content)
    elif lowered_suffix in {".js", ".mjs"}:
        matches = JS_IMPORT_URL_REGEX.findall(content)
    else:
        matches = []

    return [normalize_external_asset_url(match) for match in matches]


def iter_css_nested_asset_urls(content: str) -> list[str]:
    """Extract nested external URLs from CSS url(...) references."""
    return [normalize_external_asset_url(match) for match in CSS_NESTED_ASSET_URL_REGEX.findall(content)]


def iter_css_relative_asset_urls(content: str) -> list[str]:
    """Extract relative url(...) paths from CSS content."""
    return CSS_RELATIVE_URL_REGEX.findall(content)


def resolve_relative_css_url(relative_path: str, source_url: str) -> str:
    """Resolve a relative CSS url(...) path against the URL the CSS was fetched from."""
    return urljoin(source_url, relative_path)


def is_supported_asset_content_type(content_type: str) -> bool:
    """Return whether the HTTP content type represents a supported local asset."""
    lowered = (content_type or "").lower()
    return any(token in lowered for token in SUPPORTED_ASSET_TYPES)


def is_supported_embedded_asset_content_type(content_type: str) -> bool:
    """Return whether the HTTP content type represents a supported nested CSS asset."""
    lowered = (content_type or "").lower()
    return any(token in lowered for token in SUPPORTED_EMBEDDED_TYPES)


def infer_extension(url: str, content_type: str) -> str:
    """Infer a filesystem extension from the URL and response content type."""
    parsed = urlparse(normalize_external_asset_url(url))
    suffix = PurePosixPath(parsed.path).suffix.lower()
    if suffix:
        return suffix

    lowered = (content_type or "").lower()
    for token, extension in CONTENT_TYPE_EXTENSION_MAP.items():
        if token in lowered:
            return extension

    path_name = PurePosixPath(parsed.path).name.lower()
    if path_name == "css":
        return ".css"
    return ".js"


def build_external_asset_relative_path(url: str, content_type: str) -> str:
    """Build a deterministic relative static path for a downloaded external asset."""
    normalized_url = normalize_external_asset_url(url)
    parsed = urlparse(normalized_url)
    ext = infer_extension(normalized_url, content_type)
    host = re.sub(r"[^A-Za-z0-9._-]", "_", parsed.netloc) or "external"
    raw_name = PurePosixPath(parsed.path).name or "asset"
    stem = PurePosixPath(raw_name).stem if PurePosixPath(raw_name).suffix else raw_name
    safe_stem = re.sub(r"[^A-Za-z0-9._-]", "_", stem).strip("._") or "asset"
    digest = hashlib.sha1(normalized_url.encode("utf-8")).hexdigest()[:12]
    return f"{EXTERNAL_ASSET_ROOT}/{host}/{digest}_{safe_stem}{ext}"
