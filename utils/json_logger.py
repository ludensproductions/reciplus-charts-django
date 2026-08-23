import json
import logging
import traceback
from datetime import datetime, timezone

from django.conf import settings

logger = logging.getLogger("file_logger")

SENSITIVE_PATTERNS = ("pass", "token", "secret", "key", "auth", "session")


def _sanitize(data):
    """Recursively remove sensitive keys from log data based on sensitive patterns."""
    if isinstance(data, dict):
        return {k: _sanitize(v) for k, v in data.items() if not any(p in k.lower() for p in SENSITIVE_PATTERNS)}
    if isinstance(data, list):
        return [_sanitize(i) for i in data]
    return data


def log(data: dict):
    """Write a log entry to file."""
    data = _sanitize(data)
    data["time"] = datetime.now(timezone.utc).isoformat()
    log_entry = json.dumps(data, ensure_ascii=False, default=str)

    level = data.get("level", "ERROR").upper()
    log_method = getattr(logger, level.lower(), logger.error)
    log_method(log_entry)


def log_error(data: dict):
    """Log an error level entry with traceback."""
    data = {"level": "ERROR", **data, "traceback": traceback.format_exc()}
    log(data)


def log_warning(data: dict):
    """Log a warning level entry."""
    data = {"level": "WARNING", **data}
    log(data)


def log_info(data: dict):
    """Log an info level entry."""
    data = {"level": "INFO", **data}
    log(data)


def log_debug(data: dict):
    """Log a debug level entry, only in DEBUG mode."""
    if not settings.DEBUG:
        return
    data = {"level": "DEBUG", **data}
    log(data)


def get_error_log(request) -> dict:
    """Get the error log from the request, including the path, exception info, user, and params."""
    user = "anonymous"
    if request.user and not request.user.is_anonymous:
        user = request.user.username

    error_log = {
        "path": request.path,
        "user": user,
        "params": request.POST if request.method == "POST" else request.GET,
    }

    return error_log
