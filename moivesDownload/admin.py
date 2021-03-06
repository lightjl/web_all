from django.contrib import admin
from moivesDownload.models import Moive, People, Watch, Statue_dm, Rss
# Register your models here.

class WatchAdmin(admin.ModelAdmin):
    list_display = ('moive', 'statue')
    list_filter = ('statue',)
    fields = ('statue',)

class MoiveAdmin(admin.ModelAdmin):
    list_display = ('name_En', 'downloadLink')
    fields = ('name_Zh', 'name_En',)
    
admin.site.register(Moive, MoiveAdmin)
admin.site.register(People)
admin.site.register(Watch, WatchAdmin)
admin.site.register(Statue_dm)
admin.site.register(Rss)