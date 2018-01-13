from django.db import models

# Create your models here.

class Rask(models.Model):
    name = models.CharField(max_length=30)
    runFlag = models.BooleanField(default=0)
    webSite = models.CharField(max_length=100)
    timePeriod = models.CharField(max_length=100)
    timeRelax = models.PositiveSmallIntegerField()
    weekday = models.CharField(max_length=20)
    def __str__(self):
        return ('%s %s' % (self.name, self.timePeriod))