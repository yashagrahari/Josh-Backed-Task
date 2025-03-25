# Admin setup
from django.contrib import admin
from tasks.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'created_at')
    search_fields = ('name', 'status')
    list_filter = ('status',)
