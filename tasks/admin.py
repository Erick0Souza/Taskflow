from django.contrib import admin
from .models import Task, TaskComment, TaskEvent

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "priority", "assignee", "due_date")
    list_filter = ("status", "priority", "project")
    search_fields = ("title", "description")

admin.site.register(TaskComment)
admin.site.register(TaskEvent)
