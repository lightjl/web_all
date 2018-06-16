from django.db import models

# Create your models here.

class Book(models.Model):
    bookname = models.CharField(max_length=30)
    zz = models.CharField(max_length=30)
    tags = models.CharField(max_length=30)
    gxsj = models.CharField(max_length=14)
    rating = models.FloatField()
    cclink = models.CharField(max_length=100)
    dblink = models.CharField(max_length=100)
    bz = models.CharField(max_length=1000)
    
    def __str__(self):
        return ('%s %s %f' % (self.bookname, self.tags, self.rating))
    
class People(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return ('%s' % (self.name))
    
class Statue_dm(models.Model):
    means = models.CharField(max_length=20)
    def __str__(self):
        return ('%s' % (self.means))
    
class Read(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    statue = models.ForeignKey(Statue_dm, on_delete=models.CASCADE)
    cs = models.SmallIntegerField()
    
    def __str__(self):
        return ('%s %s %s %d' % (self.book.bookname, self.tags, self.statue.means, self.cs))