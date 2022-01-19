# Importing the libraries
from django.apps import AppConfig


class EmaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ema'
    def ready(self):
        """
        Using this function to import signals.py
        """
        import ema.signals