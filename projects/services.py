from django.db import transaction
from .models import ProjectMembership

@transaction.atomic
def add_member(project, user, role):
    membership, created = ProjectMembership.objects.update_or_create(
        project=project,
        user=user,
        defaults={"role": role},
    )
    return membership, created
