from django.shortcuts import render
from . import p_game
from django.http import HttpResponse

# Create your views here.

def Check_game(request):
    for page in range(0, 20):
        p_game.check_page(page)
    return HttpResponse('check game done')