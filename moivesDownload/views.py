from django.shortcuts import render, render_to_response

from django.http import HttpResponse
from moivesDownload.models import Moive, People, Watch, Statue_dm
from django.views.decorators.csrf import csrf_exempt   
from django.db.models import Count
from django.db.models import Q 
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')

def show(request):  # show
    ws = Watch.objects.all().values('statue__id', 'statue__means').annotate(total=Count('moive'))
    logging.debug(ws)
    
    return render_to_response('moivesDownload/list.html', 
                              {'moives':Watch.objects.filter(people__name="me"), 
                               'dms':Statue_dm.objects.filter(show=1),
                               'ws':ws
                               })


def showdm(request, dm):  # show
    ws = Watch.objects.all().values('statue__id', 'statue__means').annotate(total=Count('moive'))
    logging.debug(ws)
    leave = Statue_dm.objects.filter(id=dm)[0]
    return render_to_response('moivesDownload/list.html', 
                              {'moives':Watch.objects.filter(people__name="me", statue__id=dm), 
                               'dms':Statue_dm.objects.filter(show=1, leave__gte=leave.leave).filter(~Q(id=dm)),
                               'ws':ws
                               })


@csrf_exempt
def change(request):    # change the watch dm 改变watch的状态
    arrays = request.POST.getlist('ids[]')
    arrays = [int(x) for x in arrays]
    dmid = int(request.POST.getlist('dmid')[0])
    watchs = Watch.objects.filter(id__in=arrays)
    dm_tochange = Statue_dm.objects.filter(id=dmid)
    watchs.update(statue = dm_tochange[0])
    #print(dm_tochange[0].means)
    for w in watchs:
        logging.info(w.moive.name_En + dm_tochange[0].means)
        
    return render_to_response('moivesDownload/list.html', {'moives':Watch.objects.all(), 'dms':Statue_dm.objects.all()})