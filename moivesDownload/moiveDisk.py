# -*- coding: UTF-8 -*-
# scan moive in ~/Videos
import os
from moivesDownload.moiveE import NameEng
from moivesDownload.models import Moive, People, Watch, Statue_dm
from django.http import HttpResponse
from pathlib import Path

def ListEngNameMoive(fold):
    listMoive = (os.listdir(os.path.expanduser(fold)))
    # todo fixing next
    
    listEngNameMoive = []
    for name in listMoive:
        listEngNameMoive.append(NameEng(name).name)
    return listEngNameMoive

def ListWatched(listEngNameMoive):
    dm_inComputer = Statue_dm.objects.filter(means='在电脑')
    moiveInedComputer = Watch.objects.filter(statue__in=dm_inComputer)
    
    listWatched = [] # 已看列表
    for w in moiveInedComputer:
        if (w.moive.name_En) not in listEngNameMoive:
            # deleted
            listWatched.append(w.moive.name_En)
    
    return listWatched

def UpdateWatched(listWatched):
    dm_watched = Statue_dm.objects.filter(means='已看')
    moiveWatched = Moive.objects.filter(name_En__in=listWatched)
    watched = Watch.objects.filter(moive__in=moiveWatched)
    watched.update(statue = dm_watched[0])

def UpdateInComputer(listComputer):
    mvs = Moive.objects.filter(name_En__in=listComputer)
    dm_tochange = Statue_dm.objects.filter(means='在电脑')
    watchs = Watch.objects.filter(moive__in=mvs)
    watchs.update(statue = dm_tochange[0])

def which_pan():
    for i in range(ord('F'),ord('J')):
        fold = chr(i) + ':/a_moive_remoiveable'
        if Path(fold).exists():
            return fold
    return False

def changeWatchDm(request):
    fold = which_pan()
    if not fold:
        return
    
    listEngNameMoive = ListEngNameMoive(fold)
    # print(listEngNameMoive)
    # 更新已看完的moives
    # todo
    listWatched = ListWatched(listEngNameMoive)
    
    UpdateWatched(listWatched)
    UpdateInComputer(listEngNameMoive)
    # 标记现已在电脑的moives
    return HttpResponse("watchdm changed!")