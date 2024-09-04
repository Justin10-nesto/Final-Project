from django.apps import AppConfig


class OnlineLearningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OnlineLearning'

    def ready(self):
        import OnlineLearning.signals

