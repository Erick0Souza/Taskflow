from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from projects.views import visible_projects
from tasks.models import Task

@login_required
def home(request):
    projects = visible_projects(request.user)
    tasks = Task.objects.filter(project__in=projects)

    if not request.user.is_admin and request.user.role == "member":
        tasks = tasks.filter(Q(assignee=request.user) | Q(created_by=request.user))

    today = timezone.localdate()
    summary = tasks.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status=Task.Status.PENDING)),
        in_progress=Count("id", filter=Q(status=Task.Status.IN_PROGRESS)),
        done=Count("id", filter=Q(status=Task.Status.DONE)),
        overdue=Count("id", filter=Q(due_date__lt=today) & ~Q(status=Task.Status.DONE)),
    )

    recent_tasks = tasks.select_related("project", "assignee").order_by("-updated_at")[:8]
    return render(
        request,
        "dashboard/home.html",
        {
            "summary": summary,
            "recent_tasks": recent_tasks,
            "project_count": projects.count(),
        },
    )
