from douban.douban_find import douban_web_mx
from douban.models import db_web, db_web_mx
import datetime


db_webs = db_web.objects.all()

for item in db_webs[:]:
    doubanID = item.doubanID
    link = item.link
    mxs = db_web_mx.objects.filter(doubanID = doubanID)
    if (len(mxs) > 0):
        continue
    tmp = douban_web_mx(link)
    try:
        (doubanIDtmp, infos, tags, IMDBid, kbf, bz, rating) = tmp.douban_infos_all()
    except:
        continue
    mx = db_web_mx(doubanID=doubanID, infos=infos, tags=tags, IMDBid=IMDBid, kbf=kbf, bz=bz)
    mx.save()
    
    zb = db_web.objects.filter(doubanID = doubanID)
    zb.update(rating = float(rating), xgrq=datetime.date.today())
    
    
    
#     doubanID = models.CharField(max_length=20)
#     tags = models.CharField(max_length=30)
#     infos = models.CharField(max_length=30) # 地区、语言、集数、单集片长、又名
#     IMDBid = models.CharField(max_length=20) # IMDb链接
#     kbf = models.CharField(max_length=100) # 在哪儿看这部剧集
#     bz = models.CharField(max_length=1000)