# -*- coding: UTF-8 -*-
# scan moive in ~/Videos
import os
from moivesDownload.moiveE import NameEng
from moivesDownload.models import Moive, People, Watch, Statue_dm
from django.http import HttpResponse
from pathlib import Path

def changeWatchDm(request):
    if not Path('/media/l/TOSHIBA EXT').exists():
        return 
    listMoive = (os.listdir(os.path.expanduser('/media/l/TOSHIBA EXT')))
    
    listEngNameMoive = []
    for name in listMoive:
        listEngNameMoive.append(NameEng(name).name)
    
    # print(listEngNameMoive)
    # 更新已看完的moives
    dm_inComputer = Statue_dm.objects.filter(means='在电脑')
    dm_watched = Statue_dm.objects.filter(means='已看')
    moiveInedComputer = Watch.objects.filter(statue__in=dm_inComputer)
    
    listOut = []
    for w in moiveInedComputer:
        if (w.moive.name_En) not in listEngNameMoive:
            # deleted
            listOut.append(w.moive.name_En)
    
    moiveWatched = Moive.objects.filter(name_En__in=listOut)
    watched = Watch.objects.filter(moive__in=moiveWatched)
    watched.update(statue = dm_watched[0])
    
    # 标记现已在电脑的moives
    mvs = Moive.objects.filter(name_En__in=listEngNameMoive)
    dm_tochange = Statue_dm.objects.filter(means='在电脑')
    watchs = Watch.objects.filter(moive__in=mvs)
    watchs.update(statue = dm_tochange[0])
    return HttpResponse("watchdm changed!")