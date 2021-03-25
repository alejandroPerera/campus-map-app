#  Correctly ties our app config to Django.
#  This is no longer necessary in Django 3.2, but we're on 3.1.7 I think
default_app_config = 'map.apps.MapConfig'
