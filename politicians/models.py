from django.db import models

# Create your models here.
class Party(models.Model):
    abbr = models.CharField(max_length=20)
    english_name = models.CharField(max_length=255)
    malay_name = models.CharField(max_length=255, blank=True)
    chinese_name = models.CharField(max_length=255, blank=True)
    iban_name = models.CharField(max_length=255, blank=True)
    tamil_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.abbr
    class Meta:
        verbose_name_plural = "Parties"
class Politician(models.Model):
    name = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    othername = models.CharField(max_length=255, blank=True)
    image_url = models.TextField(blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    wikipedia = models.CharField(max_length=255, blank=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
class Constituency(models.Model):
    state = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, null=True)
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
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
