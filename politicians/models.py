from django.db import models

# Create your models here.
class Politician(models.Model):
    name = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    wikipedia = models.CharField(max_length=255)
    def __str__(self):
        return self.name
