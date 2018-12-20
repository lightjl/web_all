from django.db import models

# Create your models here.

class Nhg(models.Model):
    row_sz = models.PositiveSmallIntegerField()
    highInit = models.FloatField()
    setDate = models.DateField(auto_now=True)
    highest = models.FloatField()
    highTodayInit = models.FloatField()