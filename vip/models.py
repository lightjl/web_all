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