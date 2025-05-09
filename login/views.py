from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import cargo_necessario


def login_view(request):
    # Verifica se o usuário já está autenticado
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
        user = authenticate(request, email=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request, "login/login.html", {"erro": "Credenciais inválidas"}
            )
    return render(request, "login/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    return render(request, "paginas/home.html")


@login_required
@cargo_necessario("adm")
def admin_page(request):
    return render(request, "paginas/admin_page.html")


@login_required
@cargo_necessario("gestor")
def gestor_page(request):
    return render(request, "paginas/gestor_page.html")


@login_required
@cargo_necessario("func")
def funcionario_page(request):
    return render(request, "paginas/funcionario_page.html")
