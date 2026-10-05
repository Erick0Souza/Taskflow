def can_view_task(user, task):
    if user.is_admin or task.project.owner_id == user.id:
        return True
    return task.project.members.filter(pk=user.pk).exists()

def can_manage_task(user, task):
    if user.is_admin or task.project.owner_id == user.id:
        return True
    membership = task.project.memberships.filter(user=user).first()
    return bool(membership and membership.role == "manager")

def can_update_status(user, task):
    return can_manage_task(user, task) or task.assignee_id == user.id
