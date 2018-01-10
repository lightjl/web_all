from django.shortcuts import render, render_to_response

from django.http import HttpResponse
from moivesDownload.models import Moive, People, Watch, Statue_dm

# Create your views here.

def show(request):  # show
    
    return render_to_response('moivesDownload/list.html', {'moives':Moive.objects.all()})