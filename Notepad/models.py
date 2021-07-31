from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Notepad(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    

class Page(models.Model):
    master = models.ForeignKey(Notepad, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    body = models.TextField()
