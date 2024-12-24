# crawl/apps.py
from django.apps import AppConfig

class CrawlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crawl'

    def ready(self):
        """
        Django가 이 앱(crawl)을 로드할 때, 스케줄러를 실행
        """
        from .scheduler.articleupdater import start
        start()
