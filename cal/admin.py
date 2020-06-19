from django.contrib import admin
from cal.models import *

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'grade')
    list_display_links = ('id', 'title', 'grade')

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade')
    list_display_links = ('id', 'name', 'grade')

class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'event')
    list_display_links = ('id', 'name', 'event')

class WorkTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'challenge')
    list_display_links = ('id', 'challenge')

class WA_Admin(admin.ModelAdmin):
    list_display = ('id', 'workteam', 'activity', 'state')
    list_display_links = ('id', 'workteam', 'activity', 'state')


admin.site.register(Event, EventAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(WorkTeam, WorkTeamAdmin)
admin.site.register(workteam_activity, WA_Admin)
