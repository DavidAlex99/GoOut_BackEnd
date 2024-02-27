from django.apps import AppConfig


class GooutappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goOutApp'

# aplicacion que servira para poder recxeptar la senal
    # cuando el usuario se cree un usuario
class TuAppConfig(AppConfig):
    name = 'tu_app'

    def ready(self):
        import tu_app.signals