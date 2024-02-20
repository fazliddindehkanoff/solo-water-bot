from django.apps import AppConfig


class TgbotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tgbot"

    def ready(self) -> None:
        import tgbot.signals

        return super().ready()
