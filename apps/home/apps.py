from django.apps import AppConfig
from django.conf import settings


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.home'
    label = 'apps_home'

    # def ready(self):
    #     if settings.SCHEDULER_DEFAULT:
    #         from apps.home import backup
    #         backup.start()