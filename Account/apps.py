from django.apps import AppConfig

from Account.variables import Strings as AccountModelVerboseNameStrings


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Account'
    verbose_name = AccountModelVerboseNameStrings.app_name
