from django.db import models

# Create your models here.

class Moive(models.Model):
    name_Zh = models.CharField(max_length=30)
    name_En = models.CharField(max_length=100)
    downloadLink = models.CharField(max_length=300)
    
class People(models.Model):
    name = models.CharField(max_length=20)
    
class Statue_dm(models.Model):
    statue = models.CharField(max_length=5)
    means = models.CharField(max_length=20)
    
class Watch(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    moive = models.ForeignKey(Moive, on_delete=models.CASCADE)
    statue = models.ForeignKey(Statue_dm, on_delete=models.CASCADE)