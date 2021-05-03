from threading import Thread
import time

from django.conf import settings
from newsfilter.models import NewsCategory, NewsRecord
from .mail_helper import send_email


class Notification(Thread):
    def __init__(self):
        self.base_url = "http://localhost:8000/authenticate_news"

        super().__init__()

    def run(self):
        self.send_notification()

    def send_notification(self):
        categories = NewsCategory.objects.all()

        for cat in categories:
            data = {}

            subscribers = cat.subscribers.all()
            subscribers_email = [each.email for each in subscribers]

            news = NewsRecord.objects.filter(category=cat, sent_notification=False)

            # print(news)
            # print(cat.name)
            for each in news:
                data[each.title] = "{}/{}".format(self.base_url, each.id)
                each.sent_notification = True
                each.save()

            if data:
                send_email(to_email=subscribers_email, data=data, category=cat.name)
            else:
                print("No new news for category: {}".format(cat))
        time.sleep(600)
