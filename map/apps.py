from django.apps import AppConfig


class MapConfig(AppConfig):
    name = 'map'

    #########################
    # Reference
    # Title: Signals
    # Author: Django
    # URL:  https://docs.djangoproject.com/en/3.2/topics/signals/
    ########################
    def ready(self):
        """ Call the ready method and connect our receiver for when the database is connected """
        super(MapConfig, self).ready()
        print("Connecting connection_created signal")
        import map.signals  # Add signals.py here so the signal receiver can get its signal

