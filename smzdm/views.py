from django.shortcuts import render
from smzdm.models import mmmGame
from smzdm.mmmGame import Game
from django.http import HttpResponse

# Create your views here.

def checkGames(request):
    games = mmmGame.objects.filter(gzFlag = True)
    for game in games:
        gamePriceInfo = Game(game.id)
    return HttpResponse('checked games')
    