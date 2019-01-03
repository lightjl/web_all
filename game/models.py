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
    
    def __str__(self):
        return ('%s' % (self.name))
    
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
    
    def __str__(self):
        return ('%s' % (self.name))
    
class game_itunes(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    age = models.IntegerField()
    rating = models.FloatField()
    r_people = models.IntegerField()
    content = models.CharField(max_length=200)
    price = models.FloatField()
    in_app_purchase = models.BooleanField()
    tag = models.CharField(max_length=9)
    language = models.CharField(max_length=64)

    def __str__(self):
        return ('%s' % (self.name))