from django.db import models
from control.models import Rask

# Create your models here.

class Xs(models.Model):
    rask = models.ForeignKey(Rask, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
    
    
class Chapter(models.Model):
    name = models.CharField(max_length=30)
    xs = models.ForeignKey(Xs, on_delete=models.CASCADE)