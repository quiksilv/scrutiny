from django.db import models

from politicians.models import Politician

# Create your models here.
class Hansard(models.Model):
    name = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    raw_file = models.FileField(upload_to="hansards")
    created = models.DateField(auto_now=True)
    def __str__(self):
        return self.name
class Paragraph(models.Model):
    page = models.IntegerField()
    line = models.IntegerField()
    content = models.TextField()
    comment = models.TextField(blank=True)
    politician = models.ForeignKey(Politician, on_delete=models.SET_NULL, null=True, blank=True)
    hansard = models.ForeignKey(Hansard, on_delete=models.CASCADE)
