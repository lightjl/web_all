from django.shortcuts import render
from . import mebook
from django.http import HttpResponse
# Create your views here.

def CheckMeBook(request):
    startPage = 1
    endPage = 700
    mebook.mebook(startPage,endPage)
    return HttpResponse('follow %d-%d done' %(startPage, endPage))