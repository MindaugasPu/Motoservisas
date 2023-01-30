from django.apps import AppConfig


class MotoserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'motoservice'

    def ready(self):
        from .signals import create_profile, save_profile