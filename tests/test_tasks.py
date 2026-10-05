from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from projects.models import Project, ProjectMembership
from tasks.models import Task
from tasks.services import change_status

class TaskTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username="manager",
            password="SenhaForte123!",
            role=User.Role.MANAGER,
        )
        self.member = User.objects.create_user(
            username="member",
            password="SenhaForte123!",
            role=User.Role.MEMBER,
        )
        self.project = Project.objects.create(name="TaskFlow", owner=self.manager)
        ProjectMembership.objects.create(project=self.project, user=self.manager, role="manager")
        ProjectMembership.objects.create(project=self.project, user=self.member, role="member")

    def test_status_only_moves_forward(self):
        task = Task.objects.create(
            project=self.project,
            title="Implementar login",
            created_by=self.manager,
            assignee=self.member,
        )
        change_status(task, self.member, Task.Status.IN_PROGRESS)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)

        change_status(task, self.member, Task.Status.DONE)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.DONE)
        self.assertEqual(task.allowed_transitions(), [])

        with self.assertRaises(ValidationError):
            change_status(task, self.member, Task.Status.PENDING)

    def test_assignee_can_change_status(self):
        task = Task.objects.create(
            project=self.project,
            title="Tela inicial",
            created_by=self.manager,
            assignee=self.member,
        )
        self.client.force_login(self.member)
        response = self.client.post(
            reverse("tasks:status", args=[task.id]),
            {"status": Task.Status.IN_PROGRESS},
        )
        self.assertRedirects(response, task.get_absolute_url())
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)

    def test_member_cannot_edit_task(self):
        task = Task.objects.create(
            project=self.project,
            title="Relatório",
            created_by=self.manager,
            assignee=self.member,
        )
        self.client.force_login(self.member)
        response = self.client.get(reverse("tasks:edit", args=[task.id]))
        self.assertEqual(response.status_code, 404)
