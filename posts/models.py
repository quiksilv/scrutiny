from django.db import models
from django.contrib.auth.models import User

from politicians.models import Politician

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Post(models.Model):
    POST_STATUS = (('pending', 'pending'), ('suspended', 'suspended'), ('active', 'active'), ('deleted', 'deleted') )
    content = models.TextField(default="")
    status = models.CharField(max_length=20, choices=POST_STATUS, default="active")
    parent = models.IntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)
    def __str__(self):
        return self.content
