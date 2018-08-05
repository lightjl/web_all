from django.shortcuts import render
from . import p_game, p_BRPG
from django.http import HttpResponse

# Create your views here.

def Check_game(request):
    for page in range(0, 20):
        p_game.check_page(page)
    return HttpResponse('check game done')


def Check_BRPG(request):
    for page in range(1, 5):
        p_BRPG.check_page(page)
    return HttpResponse('check BRPG done')