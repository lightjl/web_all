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