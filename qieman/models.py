from django.db import models

# Create your models here.
class Fund(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    fs = models.FloatField()
    yk = models.FloatField()
    price_min = models.FloatField()
    price_hold = models.FloatField()
    
    fs_my = models.FloatField(null=True, blank=True)
    yk_my = models.FloatField(null=True, blank=True)
    price_min_my = models.FloatField(null=True, blank=True)
    price_hold_my = models.FloatField(null=True, blank=True)
    
    jz = models.FloatField()
    gszzl = models.FloatField(null=True, blank=True) # 估算增长率
    
    gxsj = models.DateTimeField('最后修改日期', null=True, blank=True)