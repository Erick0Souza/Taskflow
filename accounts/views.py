from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm

class SignInView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

class SignOutView(LogoutView):
    next_page = "accounts:login"

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard:home")

    return render(request, "accounts/register.html", {"form": form})
