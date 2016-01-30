from django.contrib import admin

from .models import Schedule, Message


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_before_election', 'media_type')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sent', 'voter', 'election', 'media_type')
    readonly_fields = ('sent', 'voter', 'election', 'schedule')

    def media_type(self, message):
        return message.schedule.get_media_type_display()
