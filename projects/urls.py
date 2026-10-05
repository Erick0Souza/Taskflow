from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.project_list, name="list"),
    path("novo/", views.project_create, name="create"),
    path("<int:pk>/", views.project_detail, name="detail"),
    path("<int:pk>/editar/", views.project_edit, name="edit"),
    path("<int:pk>/membros/adicionar/", views.member_add, name="member_add"),
    path("<int:pk>/membros/<int:membership_id>/remover/", views.member_remove, name="member_remove"),
]
