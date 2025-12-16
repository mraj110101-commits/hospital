# hospital/apps.py
from django.apps import AppConfig

class HospitalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital'

    def ready(self):
        # import signals so they are registered when Django starts
        # using local import to avoid import-time side effects
        try:
            import hospital.signals  # noqa: F401
        except Exception:
            # If you want to see errors during startup, remove this try/except
            pass
