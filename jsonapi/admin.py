from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class StudentEventInline(admin.TabularInline):
    model = StudentEvent

class StudentAdmin(admin.ModelAdmin):
    inlines = (StudentEventInline,)
    extra = 0

admin.site.register(Student, StudentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Event)
admin.site.register(Clinician)
admin.site.register(Tile)
admin.site.register(Config)
