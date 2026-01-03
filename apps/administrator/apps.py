from django.apps import AppConfig


class AdministratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.administrator"
    label = "administrator"
    
    def ready(self):
        import apps.administrator.signals