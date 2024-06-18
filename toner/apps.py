from django.apps import AppConfig


class TonerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'toner'
    def ready(self):
        import toner.signals