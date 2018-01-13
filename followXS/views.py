from django.shortcuts import render
from . import xs
from django.http import HttpResponse
# Create your views here.

def follow(request, id):
    myxs = xs.XS(id)
    myxs.follow()
    return HttpResponse('follow once done')