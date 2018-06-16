from django.contrib import admin

# Register your models here.

from smzdm.models import zdmWeb, zdmSp

# Register your models here.

class zdmWebAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    fields = ('name', 'url')

class zdmSpAdmin(admin.ModelAdmin):
    list_display = ('hwmc','je', 'by', 'mj', 'url', 'zqrq', 'gxsj')
    
admin.site.register(zdmWeb, zdmWebAdmin)
admin.site.register(zdmSp, zdmSpAdmin)