import os
from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = "Cria o administrador inicial se ele ainda não existir."

    def handle(self, *args, **options):
        username = os.getenv("INITIAL_ADMIN_USERNAME", "admin")
        email = os.getenv("INITIAL_ADMIN_EMAIL", "admin@taskflow.local")
        password = os.getenv("INITIAL_ADMIN_PASSWORD", "Admin@123")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Administrador inicial já existe."))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS("Administrador inicial criado."))
