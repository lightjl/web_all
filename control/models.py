from django.db import models

# Create your models here.

class Rask(models.Model):
    name = models.CharField(max_length=30)
    runFlag = models.BooleanField(default=0)
    webSite = models.CharField(max_length=100)
    timePeriod = models.CharField(max_length=100)
    timeRelax = models.PositiveSmallIntegerField()
    weekday = models.CharField(max_length=20)
    run_time_last = models.DateTimeField(null=True, blank=True)
    run_success_time_last = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return ('%s %s 最后运行时间:' % (self.name, self.timePeriod)) + \
            self.run_time_last.strftime('%d %H:%M') + ' 最后成功时间:' + self.run_success_time_last.strftime('%d %H:%M')