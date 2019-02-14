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
    year = models.IntegerField(default=0)
    gxsj = models.CharField(max_length=14)
    rating = models.FloatField()
    link = models.CharField(max_length=100)
    bz = models.CharField(max_length=1000)
    watch_status = models.CharField(max_length=9)
    
    def __str__(self):
        return ('%s %s %f' % (self.name, self.tags, self.rating))
    
class db_web(models.Model):
    name = models.CharField(max_length=30)
    link = models.CharField(max_length=100)
    rating = models.FloatField()
    doubanID = models.CharField(max_length=20)
    xs = models.CharField(max_length=10) # 形式 eg:电影电视剧综艺动漫纪录片短片
    xgrq = models.DateField(auto_now=True)
    
class db_web_mx(models.Model):
    doubanID = models.CharField(max_length=20)
    tags = models.CharField(max_length=30)
    infos = models.CharField(max_length=30) # 地区、语言、集数、单集片长、又名
    IMDBid = models.CharField(max_length=20) # IMDb链接
    kbf = models.CharField(max_length=100) # 在哪儿看这部剧集
    bz = models.CharField(max_length=1000)
    
class imdb_item(models.Model):
    Title = models.CharField(max_length=20)
    Year = models.CharField(max_length=20)
    Rated = models.CharField(max_length=20)
    Released = models.CharField(max_length=20)
    Runtime = models.CharField(max_length=20)
    Genre = models.CharField(max_length=20)
    Director = models.CharField(max_length=20)
    Writer = models.CharField(max_length=20)
    Actors = models.CharField(max_length=20)
    Plot = models.CharField(max_length=20)
    Language = models.CharField(max_length=20)
    Country = models.CharField(max_length=20)
    Awards = models.CharField(max_length=20)
    Poster = models.CharField(max_length=20)
    Metascore = models.CharField(max_length=20)
    imdbRating = models.CharField(max_length=20)
    imdbVotes = models.CharField(max_length=20)
    imdbID = models.CharField(max_length=20)
    Type = models.CharField(max_length=20)
    totalSeasons = models.CharField(max_length=20)
    