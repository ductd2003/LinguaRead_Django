from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        from myapp.scheduler import start_scheduler
        from django.db.models.signals import post_migrate

        # Gọi start_scheduler sau khi Django hoàn tất migration
        def start_scheduler_after_migrate(sender, **kwargs):
            start_scheduler()

        post_migrate.connect(start_scheduler_after_migrate, sender=self)
