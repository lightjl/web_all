from django.db import models

# Create your models here.
class gsy(models.Model):
    name = models.CharField(max_length=30)
    lb = models.CharField(max_length=6)
    sl = models.IntegerField(default=0)
    nlq = models.IntegerField(default=0)
    nlz = models.IntegerField(default=6)
    bfl_w = models.IntegerField(default=0) # 播放量
    url = models.CharField(max_length=30)
    bz = models.CharField(max_length=30)
    gxsj = models.DateField(auto_now=True)
