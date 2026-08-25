class AppConstants:
    """App labels owned by hsl-7-common (reciplus-djangoninja's shared schema)."""

    SHARED_APPS = {"user", "hsl_7"}


class DatabaseRouter:
    """Blocks migrations for the apps that live in hsl-7-common: their schema is
    owned by common/django/migrator (a separate project), not by this one — running
    migrate/makemigrations here for them would try to alter tables this project
    doesn't own."""

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in AppConstants.SHARED_APPS:
            return False
        return None
