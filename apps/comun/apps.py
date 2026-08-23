import logging
import sys
import time

from django.apps import AppConfig, apps
from django.db import connections
from django.db.utils import OperationalError

from .consts import PermissionCode

logger = logging.getLogger(__name__)


class ComunConfig(AppConfig):
    """Configure the comun app and patch permission display strings."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.comun"

    def ready(self):
        """Run initialization hooks for the app.

        This runs once when Django boots, no matter which server or command
        triggered it.
        """
        Permission = apps.get_model("auth", "Permission")
        self.patch_permission_str(Permission)

        # Skip the check for commands that do not need the database
        # (collectstatic, makemigrations, etc.)
        if self._is_management_command_exempt():
            return

        self._wait_for_database()

    def patch_permission_str(self, Permission):
        """Patch Django's Permission string representation.

        This uses the localized permission labels defined in constants.
        """
        action_map = {
            "add": f"{PermissionCode.CAN} {PermissionCode.ADD}",
            "change": f"{PermissionCode.CAN} {PermissionCode.CHANGE}",
            "delete": f"{PermissionCode.CAN} {PermissionCode.DELETE}",
            "view": f"{PermissionCode.CAN} {PermissionCode.VIEW}",
            "enable": f"{PermissionCode.CAN} {PermissionCode.ENABLE}",
            "disable": f"{PermissionCode.CAN} {PermissionCode.DISABLE}",
        }

        def permission_str(self):
            parts = self.codename.split("_", 1)

            if len(parts) == 2:
                action, model = parts
                if action in action_map:
                    return f"{action_map[action]} {self.content_type.model_class()._meta.verbose_name.lower()}"

            # Fallback to the default permission name.
            return f"{self.content_type} | {self.name}"

        Permission.__str__ = permission_str

    def _wait_for_database(self):
        """Block startup until every configured database answers.

        Aborts the process when a database stays unreachable, so the
        orchestrator can tell the service failed to start.
        """
        max_retries = 5  # Keep it bounded so startup cannot hang forever
        retry_delay = 2  # Seconds between attempts

        for db_name in connections:
            for attempt in range(max_retries):
                try:
                    # Force the connection to the database
                    connections[db_name].ensure_connection()
                    logger.info('Database "%s" ready', db_name)
                    break  # Stop retrying once the connection succeeds
                except OperationalError:
                    if attempt < max_retries - 1:
                        logger.warning(
                            'Database "%s" unavailable, waiting %d seconds...',
                            db_name,
                            retry_delay,
                        )
                        time.sleep(retry_delay)
                    else:
                        logger.exception(
                            'CRITICAL ERROR: database "%s" is unavailable '
                            "after %d attempts. Aborting application startup.",
                            db_name,
                            max_retries,
                        )
                        # Exit with an error code so the orchestrator
                        # (Docker, Supervisor, Bash) knows the service failed.
                        sys.exit(1)

    def _is_management_command_exempt(self):
        """Skip the database check for maintenance management commands.

        These commands do not need a live database connection.
        """
        if len(sys.argv) > 1:
            exempt_commands = [
                "collectstatic",
                "makemigrations",
                "help",
                "version",
            ]
            return any(cmd in sys.argv for cmd in exempt_commands)
        return False
