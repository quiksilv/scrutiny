from django.db import models

from politicians.models import Politician
# Create your models here.
class Source(models.Model):
    SOURCE_TYPES = (('agg', 'agg'), ('scrap', 'scrap'))
    name = models.CharField(max_length=255)
    rss = models.TextField()
    type = models.CharField(max_length=10, choices=SOURCE_TYPES, default="agg")
    image = models.ImageField(upload_to="logos", null=True)
    def __str__(self):
        return self.name

class Agency(models.Model):
    headline = models.TextField(default="")
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    published = models.DateTimeField()
    link = models.TextField(blank=True)
    first_image_url = models.TextField(blank=True)
    guid = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    politician = models.ManyToManyField(Politician, blank=True)
    def __str__(self):
        return self.headline
    class Meta:
        verbose_name_plural = "Agencies"
