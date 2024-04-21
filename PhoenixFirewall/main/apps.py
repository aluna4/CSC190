from django.apps import AppConfig

class MainConfig(AppConfig):
    # set the default auto field to use for models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    
    # set the name of the app
    name = 'main'
