from django.db import models

# Create your models here.

class zdmWeb(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    gxFlag = models.BooleanField()
    
    def __str__(self):
        return ('%s' % (self.name))
    
class zdmSp(models.Model):
    hwmc = models.CharField(max_length=46)
    je = models.FloatField()
    mj = models.BooleanField()
    by = models.BooleanField()
    zqrq = models.DateField(auto_now=True)
    bz = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    gxsj = models.CharField(max_length=100)
    
class mmmGame(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=600)
    tbUrl = models.CharField(max_length=400)
    ce = models.FloatField(null=True, blank=True)
    lowerPrice = models.FloatField(null=True, blank=True)
    lowerDate = models.CharField(max_length=10, null=True, blank=True)
    currentPrice = models.FloatField(null=True, blank=True)
    currentDate = models.DateField(auto_now=False)
    gzFlag = models.BooleanField()
    buyPrice = models.FloatField()
    yj = models.FloatField()
    cb = models.FloatField()