from django.contrib import admin
from game.models import game, BRPG

# Register your models here.
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'tag', 'platform', 'esrb', 'content_descriptors')
    
admin.site.register(game, GameAdmin)

class BRPGAdmin(admin.ModelAdmin):
    list_display = ('name', 'peoples', 'mins', 'hard', 'rating', 'age', 'publish_year', 'language', 'tag', 'price', 'url_tb')
    
admin.site.register(BRPG, BRPGAdmin)