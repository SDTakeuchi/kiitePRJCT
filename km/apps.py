from django.apps import AppConfig


class KmConfig(AppConfig):
    name = 'km'

    def ready(self):
        import km.signals