from django.contrib import admin
from email_os.models import Subject, Topic

# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'minutes_delay', 'deadline', 'delay_until')
    # fields = ('bookname', 'rating', 'tags', 'cclink', 'dblink', 'bz')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'cover', 'txt')
    
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topic, TopicAdmin)
