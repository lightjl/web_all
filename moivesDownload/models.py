from django.db import models

# Create your models here.

class Moive(models.Model):
    name_Zh = models.CharField(max_length=30)
    name_En = models.CharField(max_length=100)
    downloadLink = models.CharField(max_length=3000)
    
    def __str__(self):
        return ('%s' % (self.name_En))
    
class People(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return ('%s' % (self.name))
    
class Statue_dm(models.Model):
    leave = models.CharField(max_length=1)
    show = models.BooleanField(default=1)
    means = models.CharField(max_length=20)
    def __str__(self):
        return ('%s' % (self.means))
    
class Watch(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    moive = models.ForeignKey(Moive, on_delete=models.CASCADE)
    statue = models.ForeignKey(Statue_dm, on_delete=models.CASCADE)
    
    def __str__(self):
        return ('%s %s' % (self.moive.name_En, self.statue.means))
    
class Wish_list(models.Model):
    name = models.CharField(max_length=20)
    moive_id = models.IntegerField(default=0)
    watch_status = models.CharField(max_length=9)
    

class Rss(models.Model):
    name = models.CharField(max_length=10)
    rss_url = models.CharField(max_length=100)
    def __str__(self):
        return ('%s' % (self.name))