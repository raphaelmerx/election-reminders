from django.contrib import admin

from .models import Election

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'state')
