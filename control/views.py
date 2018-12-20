from django.shortcuts import render, render_to_response

from django.http import HttpResponse
from moivesDownload.models import Moive, People, Watch, Statue_dm
from django.views.decorators.csrf import csrf_exempt   
from django.db.models import Count
from django.db.models import Q 
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')
from control.models import Rask
import requests
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('control.add_rask', raise_exception=True) # app + 
def show(request):  # show
    logging.critical(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #return HttpResponse('Don\'t say hello')
    rasks = Rask.objects.all()
    return render_to_response('control/list.html', {'rasks':rasks})

@csrf_exempt
def change(request, id):  # show
    logging.critical(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    runflag = (request.POST.getlist('runFlag')[0])
    #print(runflag)
    rask = Rask.objects.get(id=id)
    rask.runFlag = (runflag == 'true')
    rask.save()
    return HttpResponse(id)

def run(request, id):  # run once
    logging.critical(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #print(runflag)
    rask = Rask.objects.get(id=id)
    session = requests.Session()
    session.get(rask.webSite)
    return HttpResponse(id)
