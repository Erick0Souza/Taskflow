from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MembershipForm, ProjectForm
from .models import Project, ProjectMembership
from .services import add_member

def visible_projects(user):
    if user.is_admin:
        return Project.objects.all()
    return Project.objects.filter(
        Q(owner=user) | Q(members=user)
    ).distinct()

@login_required
def project_list(request):
    query = request.GET.get("q", "").strip()
    projects = visible_projects(request.user).select_related("owner")
    if query:
        projects = projects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    page = Paginator(projects.order_by("name"), 12).get_page(request.GET.get("page"))
    return render(request, "projects/list.html", {"page": page, "query": query})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(
        visible_projects(request.user).select_related("owner").prefetch_related("memberships__user"),
        pk=pk,
    )
    tasks = project.tasks.select_related("assignee", "created_by").order_by("status", "due_date", "-created_at")[:20]
    membership_form = MembershipForm()
    return render(
        request,
        "projects/detail.html",
        {
            "project": project,
            "tasks": tasks,
            "membership_form": membership_form,
        },
    )

@login_required
def project_create(request):
    if not (request.user.is_admin or request.user.role == "manager"):
        raise Http404

    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        ProjectMembership.objects.get_or_create(
            project=project,
            user=request.user,
            defaults={"role": ProjectMembership.Role.MANAGER},
        )
        messages.success(request, "Projeto criado.")
        return redirect(project)
    return render(request, "projects/form.html", {"form": form, "title": "Novo projeto"})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not project.can_manage(request.user):
        raise Http404

    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Projeto atualizado.")
        return redirect(project)
    return render(request, "projects/form.html", {"form": form, "title": "Editar projeto"})

@login_required
def member_add(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not project.can_manage(request.user):
        raise Http404

    if request.method != "POST":
        return redirect(project)

    form = MembershipForm(request.POST)
    if form.is_valid():
        add_member(project, form.cleaned_data["user"], form.cleaned_data["role"])
        messages.success(request, "Membro adicionado.")
    else:
        messages.error(request, "Não foi possível adicionar o membro.")
    return redirect(project)

@login_required
def member_remove(request, pk, membership_id):
    project = get_object_or_404(Project, pk=pk)
    if not project.can_manage(request.user):
        raise Http404
    if request.method == "POST":
        membership = get_object_or_404(ProjectMembership, pk=membership_id, project=project)
        if membership.user_id == project.owner_id:
            messages.error(request, "O responsável pelo projeto não pode ser removido.")
        else:
            membership.delete()
            messages.success(request, "Membro removido.")
    return redirect(project)
