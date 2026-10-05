from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from projects.models import Project
from projects.views import visible_projects
from .forms import CommentForm, TaskForm
from .models import Task, TaskComment, TaskEvent
from .permissions import can_manage_task, can_update_status, can_view_task
from .services import change_status

@login_required
def task_list(request):
    tasks = Task.objects.filter(project__in=visible_projects(request.user)).select_related("project", "assignee")
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")

    if q:
        tasks = tasks.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if status in Task.Status.values:
        tasks = tasks.filter(status=status)
    if priority in Task.Priority.values:
        tasks = tasks.filter(priority=priority)

    page = Paginator(tasks, 20).get_page(request.GET.get("page"))
    return render(
        request,
        "tasks/list.html",
        {
            "page": page,
            "q": q,
            "status": status,
            "priority": priority,
            "statuses": Task.Status.choices,
            "priorities": Task.Priority.choices,
        },
    )

@login_required
def my_tasks(request):
    tasks = Task.objects.filter(assignee=request.user).select_related("project").order_by("status", "due_date")
    return render(request, "tasks/my_tasks.html", {"tasks": tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(
        Task.objects.select_related("project", "assignee", "created_by"),
        pk=pk,
    )
    if not can_view_task(request.user, task):
        raise Http404

    comments = task.comments.select_related("author")
    events = task.events.select_related("actor")[:20]
    comment_form = CommentForm()
    return render(
        request,
        "tasks/detail.html",
        {
            "task": task,
            "comments": comments,
            "events": events,
            "comment_form": comment_form,
            "can_manage": can_manage_task(request.user, task),
            "can_change_status": can_update_status(request.user, task),
        },
    )

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not project.can_manage(request.user):
        raise Http404

    form = TaskForm(request.POST or None, project=project)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.created_by = request.user
        task.save()
        TaskEvent.objects.create(task=task, actor=request.user, description="Tarefa criada.")
        messages.success(request, "Tarefa criada.")
        return redirect(task)
    return render(request, "tasks/form.html", {"form": form, "title": "Nova tarefa", "project": project})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task.objects.select_related("project"), pk=pk)
    if not can_manage_task(request.user, task):
        raise Http404

    form = TaskForm(request.POST or None, instance=task, project=task.project)
    if request.method == "POST" and form.is_valid():
        form.save()
        TaskEvent.objects.create(task=task, actor=request.user, description="Dados da tarefa atualizados.")
        messages.success(request, "Tarefa atualizada.")
        return redirect(task)
    return render(request, "tasks/form.html", {"form": form, "title": "Editar tarefa", "project": task.project})

@login_required
def task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not can_update_status(request.user, task):
        raise Http404
    if request.method == "POST":
        try:
            change_status(task, request.user, request.POST.get("status"))
            messages.success(request, "Status atualizado.")
        except ValidationError as exc:
            messages.error(request, exc.messages[0])
    return redirect(task)

@login_required
def comment_add(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not can_view_task(request.user, task):
        raise Http404

    if request.method == "POST" and task.status != Task.Status.DONE:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, "Comentário adicionado.")
    return redirect(task)
