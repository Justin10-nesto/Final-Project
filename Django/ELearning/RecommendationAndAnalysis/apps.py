from django.apps import AppConfig


class RecommendationandanalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'RecommendationAndAnalysis'

    def ready(self):
        import RecommendationAndAnalysis.signals
