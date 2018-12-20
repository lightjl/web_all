from django.shortcuts import render
from . import xjgl
from django.http import HttpResponse
# Create your views here.


def watch(request, id):
    xjgl.watch(id)
    return HttpResponse('watch xjgl once done')