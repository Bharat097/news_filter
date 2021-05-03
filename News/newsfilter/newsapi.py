import requests
import time

from datetime import datetime, timedelta
from threading import Thread


from django.conf import settings
from newsfilter.models import NewsRecord, NewsCategory


class NewsAPIApi(Thread):
    def __init__(self):

        self.base_url = "https://newsapi.org/v2"
        self.api_key = settings.NEWSAPI_API_KEY
        # self.last_fetch_time = (datetime.utcnow() - timedelta(days=1)).strftime(
        #     "%Y-%m-%dT%H:%M:%S"
        # )
        self.categories = [
            "business",
            "entertainment",
            "general",
            "health",
            "science",
            "sports",
            "technology"
        ]

        self.header = {"X-Api-Key": self.api_key}
        super().__init__()

    def run(self):
        self.fetch_news()

    def fetch_news(self):

        while True:
            endpoint = "/top-headlines"
            url = "{}{}".format(self.base_url, endpoint)
            params = {
                # "from": self.last_fetch_time,
                "language": "en",
                # "qInTitle": " OR ".join(words),
            }

            try:
                # print(url)
                # print(params)
                # fetched_at = datetime.utcnow()
                for category in self.categories:
                    category_obj, _ = NewsCategory.objects.get_or_create(name=category)
                    params["category"] = category
                    response = requests.get(url, headers=self.header, params=params)

                    if response.ok:
                        response = response.json()
                        articles = response.get("articles")[:1]
                        # print("{} \n {}".format(datetime.utcnow(), articles))
                        for article in articles:
                            news_record = NewsRecord(
                                author=article.get("author"),
                                title=article.get("title"),
                                description=article.get("description"),
                                news_url=article.get("news_url"),
                                published_at=article.get("published_at"),
                                news_content=article.get("news_content"),
                                api_used="NewsAPI",
                                category=category_obj
                            )
                            news_record.save()
                    else:
                        response.raise_for_status()

                # self.last_fetch_time = fetched_at.strftime("%Y-%m-%dT%H:%M:%S")
            except Exception as e:
                print(str(e))

            time.sleep(300)
