from django.db import models

# Create your models here.
class game(models.Model):
    name = models.CharField(max_length=46)
    name_eng = models.CharField(max_length=64)
    rating =  models.FloatField()
    tag = models.CharField(max_length=46)
    platform = models.CharField(max_length=46)
    esrb = models.IntegerField(default=3)
    content_descriptors = models.CharField(max_length=200)
    review_date = models.DateField()
    series = models.IntegerField(default=0)
    
class BRPG(models.Model):
    name = models.CharField(max_length=19)
    name_eng = models.CharField(max_length=46)
    href_game = models.CharField(max_length=64)
    peoples = models.CharField(max_length=9)
    mins = models.CharField(max_length=9)
    hard = models.CharField(max_length=9)
    hard_level = models.FloatField()
    rating = models.FloatField()
    tb =models.BooleanField()
    age = models.IntegerField()
    publish_year = models.IntegerField()
    language = models.CharField(max_length=19)
    tag = models.CharField(max_length=100)
    url_tb = models.CharField(max_length=100)
    price = models.FloatField()