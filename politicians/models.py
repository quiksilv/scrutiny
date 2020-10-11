from django.db import models

# Create your models here.
class Politician(models.Model):
    name = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    othername = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    wikipedia = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name
