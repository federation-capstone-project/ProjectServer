from django.contrib import admin

# Register your models here.

from .models import *

class StudentEventAdmin(admin.ModelAdmin):
     list_filter = ('event', 'student')

admin.site.register(Event)#, EventAdmin)
admin.site.register(StudentEvent, StudentEventAdmin)
admin.site.register(Student)
admin.site.register(Clinician)
