from django.db import models

# Create your models here.

class zdmWeb(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    
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