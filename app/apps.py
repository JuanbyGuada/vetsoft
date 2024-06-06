from django.apps import AppConfig


class AppConfig(AppConfig):
    '''esta clase es la que se encarga de la configuración de la aplicación'''
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
