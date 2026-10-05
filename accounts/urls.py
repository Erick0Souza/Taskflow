from django.urls import path
from .views import SignInView, SignOutView, register

app_name = "accounts"

urlpatterns = [
    path("entrar/", SignInView.as_view(), name="login"),
    path("sair/", SignOutView.as_view(), name="logout"),
    path("cadastro/", register, name="register"),
]
