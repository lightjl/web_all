from django.db import models

# Create your models here.

class Book_SN(models.Model):
    name = models.CharField(max_length=30)
    zz = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    bz = models.CharField(max_length=10)
    book_id = models.CharField(max_length=6)

    def __str__(self):
        return ('%s' % (self.name))
    
class Moive_vip(models.Model):
    name = models.CharField(max_length=30)
    zz = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    bz = models.CharField(max_length=10)
    moive_id = models.CharField(max_length=6)
    price = models.IntegerField(default=0)

    def __str__(self):
        return ('%s' % (self.name))
    
class Moive_bilibili(models.Model):
    moive_name = models.CharField(max_length=10)
    zz = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=30)
    moive_id = models.CharField(max_length=6)
    bz = models.CharField(max_length=10)
    
    def __str__(self):
        return ('%s' % (self.moive_name))