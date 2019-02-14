from douban.models import db_web, db_web_mx, imdb_item
from django.db.models import Q
from douban.douban_find import imdb_info


db_web_mxs = db_web_mx.objects.filter(~Q(IMDBid = ''))

for item in db_web_mxs[:]:
    IMDBid= item.IMDBid
    items = imdb_item.objects.filter(imdbID = IMDBid)
    if (len(items)>0):
        continue
    tmp = imdb_info(id=IMDBid)
    result = tmp.imdb_infos()
    if (result):
        (Title, Year, Rated, Released, Runtime, Genre, Director, Writer, \
                Actors, Plot, Language, Country, Awards, Poster, Metascore, \
                imdbRating, imdbVotes, imdbID, Type, totalSeasons) = result
    else:
        continue
    items = imdb_item(Title = Title, Year = Year, Rated = Rated, Released = Released, Runtime = Runtime,\
                       Genre = Genre, Director = Director, Writer = Writer, Actors = Actors, \
                       Plot = Plot, Language = Language, Country = Country, Awards = Awards, \
                       Poster = Poster, Metascore = Metascore, imdbRating = imdbRating, \
                       imdbVotes = imdbVotes, imdbID = imdbID, Type = Type, totalSeasons = totalSeasons)
    items.save()