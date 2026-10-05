from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.task_list, name="list"),
    path("minhas/", views.my_tasks, name="my"),
    path("projeto/<int:project_id>/nova/", views.task_create, name="create"),
    path("<int:pk>/", views.task_detail, name="detail"),
    path("<int:pk>/editar/", views.task_edit, name="edit"),
    path("<int:pk>/status/", views.task_status, name="status"),
    path("<int:pk>/comentarios/", views.comment_add, name="comment_add"),
]
