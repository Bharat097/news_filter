import requests
import time

from datetime import datetime, timedelta
from threading import Thread


from django.conf import settings
from newsfilter.models import NewsRecord, NewsCategory


class NewsDataApi(Thread):
    def __init__(self):

        self.base_url = "https://newsdata.io/api/1"
        self.api_key = settings.NEWSDATA_API_KEY
        # self.last_fetch_time = (
        #     datetime.utcnow() - timedelta(days=1)
        # ).strftime("%Y-%m-%dT%H:%M:%S")
        # self.header = {
        #     "X-Api-Key": self.api_key
        # }
        self.categories = [
            "business",
            "entertainment",
            "top",
            "health",
            "science",
            "sports",
            "technology"
        ]
        super().__init__()

    def run(self):
        self.fetch_news()

    def fetch_news(self):

        while True:
            endpoint = "/news"
            url = "{}{}".format(self.base_url, endpoint)
            params = {
                # "from_date": self.last_fetch_time,
                "language": "en",
                "apikey": self.api_key
                # "qInTitle": "'Apple' 'Google' 'Elon Musk' 'IPL'"
            }

            try:
                for category in self.categories:
                    category_obj, _ = NewsCategory.objects.get_or_create(name=category)
                    params["category"] = category
                    response = requests.get(url, params=params)

                    if response.ok:
                        response = response.json()
                        articles = response.get("results")[:1]
                        for article in articles:
                            news_record = NewsRecord(
                                author=article.get("creator"),
                                title=article.get("title"),
                                description=article.get("description"),
                                news_url=article.get("link"),
                                published_at=article.get("pubDate"),
                                news_content=article.get("news_content"),
                                api_used="NewsData",
                                category=category_obj
                            )
                            news_record.save()
                    else:
                        response.raise_for_status()

            except Exception as e:
                print(str(e))

            time.sleep(300)
