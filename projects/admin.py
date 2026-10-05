from django.contrib import admin
from .models import Project, ProjectMembership

class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description", "owner__username")
    inlines = [ProjectMembershipInline]
