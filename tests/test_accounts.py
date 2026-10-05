from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class AccountTests(TestCase):
    def test_register_creates_member_and_logs_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "erick",
                "first_name": "Erick",
                "email": "ERICK@example.com",
                "password1": "SenhaForte123!",
                "password2": "SenhaForte123!",
            },
        )
        self.assertRedirects(response, reverse("dashboard:home"))
        user = User.objects.get(username="erick")
        self.assertEqual(user.email, "erick@example.com")
        self.assertEqual(user.role, User.Role.MEMBER)

    def test_login_page_opens(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrar")
