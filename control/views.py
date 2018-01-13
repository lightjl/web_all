from django.shortcuts import render, render_to_response

from django.http import HttpResponse
from moivesDownload.models import Moive, People, Watch, Statue_dm
from django.views.decorators.csrf import csrf_exempt   
from django.db.models import Count
from django.db.models import Q 
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')


def test(request):  # show
    logging.critical(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return HttpResponse('Don\'t say hello')

