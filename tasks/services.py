from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Task, TaskEvent

@transaction.atomic
def change_status(task, actor, new_status):
    allowed = task.allowed_transitions()
    if new_status not in allowed:
        raise ValidationError("Transição de status inválida.")

    previous = task.get_status_display()
    task.status = new_status
    task.save(update_fields=["status", "updated_at"])

    TaskEvent.objects.create(
        task=task,
        actor=actor,
        description=f"Status alterado de {previous} para {task.get_status_display()}.",
    )
    return task
