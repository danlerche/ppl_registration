from django.contrib import admin
from .models import User, Event, Registration

class RegAdmin(admin.ModelAdmin):
    fields = ['event_name','user_name','wait_list']
    list_display = ('event_name', 'user_name', 'wait_list', 'registration_date')
    list_filter = ['event_name']

admin.site.register(Registration, RegAdmin)
admin.site.register(Event)
