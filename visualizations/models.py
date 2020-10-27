from django.db import models
from politicians.models import Politician

# Create your models here.
class Statistics(models.Model):
    TYPES = (('tweets', 'tweets'), ('fbposts', 'fbposts'), ('wikipedia', 'wikipedia'))
    category = models.CharField(max_length=10, choices=TYPES, default="tweets")
    #followers_count, following_count, tweet_count
    name = models.CharField(max_length=10)
    value = models.IntegerField(default=0)
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Statistics"
