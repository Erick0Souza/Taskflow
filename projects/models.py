from django.conf import settings
from django.db import models
from django.urls import reverse

class Project(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_projects",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProjectMembership",
        related_name="projects",
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=("owner", "is_active")),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:detail", args=[self.pk])

    def can_manage(self, user):
        return user.is_authenticated and (user.is_admin or self.owner_id == user.id)

class ProjectMembership(models.Model):
    class Role(models.TextChoices):
        MANAGER = "manager", "Gerente"
        MEMBER = "member", "Membro"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("project", "user"), name="unique_project_member")
        ]
        indexes = [
            models.Index(fields=("project", "role")),
            models.Index(fields=("user", "role")),
        ]

    def __str__(self):
        return f"{self.project} - {self.user}"
