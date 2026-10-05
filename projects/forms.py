from django import forms
from accounts.models import User
from .models import Project, ProjectMembership

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "is_active")
        labels = {
            "name": "Nome",
            "description": "Descrição",
            "is_active": "Projeto ativo",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

class MembershipForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True).order_by("first_name", "username"),
        label="Usuário",
    )
    role = forms.ChoiceField(
        choices=ProjectMembership.Role.choices,
        label="Papel no projeto",
    )
