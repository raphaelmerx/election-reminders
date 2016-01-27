from django.contrib import admin

from .models import Voter


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'state')
