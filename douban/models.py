from django.db import models

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=30)
    zz = models.CharField(max_length=30)
    tags = models.CharField(max_length=30)
    gxsj = models.CharField(max_length=14)
    rating = models.FloatField()
    link = models.CharField(max_length=100)
    bz = models.CharField(max_length=1000)
    
    def __str__(self):
        return ('%s %s %f' % (self.name, self.tags, self.rating))
    

class Moive(models.Model):
    name = models.CharField(max_length=30)
    zz = models.CharField(max_length=30)
    tags = models.CharField(max_length=30)
    gxsj = models.CharField(max_length=14)
    rating = models.FloatField()
    link = models.CharField(max_length=100)
    bz = models.CharField(max_length=1000)
    
    def __str__(self):
        return ('%s %s %f' % (self.name, self.tags, self.rating))