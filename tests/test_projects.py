from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from projects.models import Project, ProjectMembership

class ProjectTests(TestCase):
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

    def test_manager_can_create_project(self):
        self.client.force_login(self.manager)
        response = self.client.post(
            reverse("projects:create"),
            {"name": "Site novo", "description": "Projeto interno", "is_active": "on"},
        )
        self.assertEqual(response.status_code, 302)
        project = Project.objects.get(name="Site novo")
        self.assertEqual(project.owner, self.manager)

    def test_member_cannot_open_project_creation(self):
        self.client.force_login(self.member)
        response = self.client.get(reverse("projects:create"))
        self.assertEqual(response.status_code, 404)

    def test_owner_can_add_member(self):
        project = Project.objects.create(name="API", owner=self.manager)
        ProjectMembership.objects.create(project=project, user=self.manager, role="manager")
        self.client.force_login(self.manager)
        response = self.client.post(
            reverse("projects:member_add", args=[project.id]),
            {"user": self.member.id, "role": "member"},
        )
        self.assertRedirects(response, project.get_absolute_url())
        self.assertTrue(ProjectMembership.objects.filter(project=project, user=self.member).exists())
