from django.contrib import admin

from .models import Schedule, Message


admin.site.register(Message)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_before_election', 'media_type')
