from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="owned_projects", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="ProjectMembership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("manager", "Gerente"), ("member", "Membro")], default="member", max_length=20)),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="projects.project")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="members",
            field=models.ManyToManyField(related_name="projects", through="projects.ProjectMembership", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name="projectmembership",
            constraint=models.UniqueConstraint(fields=("project", "user"), name="unique_project_member"),
        ),
        migrations.AddIndex(
            model_name="project",
            index=models.Index(fields=["owner", "is_active"], name="projects_pr_owner_i_70366c_idx"),
        ),
        migrations.AddIndex(
            model_name="projectmembership",
            index=models.Index(fields=["project", "role"], name="projects_pr_project_20e178_idx"),
        ),
        migrations.AddIndex(
            model_name="projectmembership",
            index=models.Index(fields=["user", "role"], name="projects_pr_user_id_657d91_idx"),
        ),
    ]
