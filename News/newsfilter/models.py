from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class NewsCategory(models.Model):
    name = models.CharField(max_length=128)
    subscribers = models.ManyToManyField(User)


class NewsRecord(models.Model):
    author = models.CharField(max_length=128, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    news_url = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    api_used = models.CharField(max_length=128)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True)
    sent_notification = models.BooleanField(default=False)
    authentic_count = models.IntegerField(default=0)
    fake_count = models.IntegerField(default=0)
