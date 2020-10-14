from django.db import models

# Create your models here.
class Constituency(models.Model):
    state = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    wikipedia = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.state + ' ' + self.name
    class Meta:
        verbose_name_plural = "Constituencies"
class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    othername = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
class Politician(models.Model):
    name = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    othername = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    wikipedia = models.CharField(max_length=255, blank=True)
    constituency = models.ManyToManyField(Constituency, null=True)
    portfolio = models.ManyToManyField(Portfolio, null=True)
    def __str__(self):
        return self.name
