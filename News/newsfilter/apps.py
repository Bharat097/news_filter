from django.apps import AppConfig


class NewsfilterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsfilter'

    def ready(self):
        from newsfilter.newsapi import NewsAPIApi
        from newsfilter.newsdata import NewsDataApi

        n1 = NewsAPIApi()
        n2 = NewsDataApi()

        n1.start()
        n2.start()
