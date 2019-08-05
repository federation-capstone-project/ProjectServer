from django.contrib import admin

# Register your models here.

from .models import *

class EventAdmin(admin.ModelAdmin):
    StudentEvent.list_filter = ('event')

admin.site.register(Event, EventAdmin)
admin.site.register(StudentEvent)
admin.site.register(Student)
admin.site.register(Clinician)
