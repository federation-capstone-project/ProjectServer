from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import *

# class StudentEventAdmin(admin.ModelAdmin):
#      list_filter = ('event', 'student')

class StudentEventInline(admin.TabularInline):
    model = StudentEvent

class StudentAdmin(admin.ModelAdmin):
    inlines = (StudentEventInline,)
    extra = 0

admin.site.register(Student, StudentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Event)#, EventAdmin)
#admin.site.register(StudentEvent, StudentEventAdmin)
admin.site.register(Clinician)
admin.site.register(Tile)
