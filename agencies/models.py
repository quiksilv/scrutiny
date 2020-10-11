from django.db import models

from politicians.models import Politician
# Create your models here.
class Source(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Agency(models.Model):
    headline = models.TextField(default="")
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    published = models.DateTimeField()
    link = models.TextField(default="")
    guid = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    politician = models.ManyToManyField(Politician, blank=True)
    def __str__(self):
        return self.headline
    class Meta:
        verbose_name_plural = "Agencies"
