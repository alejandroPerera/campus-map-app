from django.apps import AppConfig
from django.db.backends.signals import connection_created
from map.signals import update_classes


class MapConfig(AppConfig):
    name = 'map'

    def ready(self):
        """ Call the ready method and connect our receiver for when the database is connected """
        super(MapConfig, self).ready()
        connection_created.connect(update_classes)
        print("Hi our custom ready function ran!")
