from django.db import models

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=20)
    minutes_delay = models.IntegerField(default=10)
    deadline = models.DateTimeField(null=True, blank=True)
    delay_until = models.DateTimeField()
    
class Topic(models.Model):
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    cover = models.BooleanField()
    txt = models.CharField(max_length=140)