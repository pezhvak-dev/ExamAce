from django.apps import AppConfig
from Home.variables import Strings as HomeModelVerboseNameStrings


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Home'
    verbose_name = HomeModelVerboseNameStrings.home
