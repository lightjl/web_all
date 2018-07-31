from django.contrib import admin
from game.models import game

# Register your models here.
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'tag', 'platform', 'esrb', 'content_descriptors')
    
admin.site.register(game, GameAdmin)