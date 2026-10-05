from django import forms
from .models import Task, TaskComment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "priority", "assignee", "due_date")
        labels = {
            "title": "Título",
            "description": "Descrição",
            "priority": "Prioridade",
            "assignee": "Responsável",
            "due_date": "Prazo",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            self.fields["assignee"].queryset = project.members.filter(is_active=True).order_by("first_name", "username")

class CommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ("body",)
        labels = {"body": "Comentário"}
        widgets = {"body": forms.Textarea(attrs={"rows": 3})}
