from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
        user = authenticate(request, email=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect(reverse("pagina_inicial"))
        else:
            return render(
                request, "login/login.html", {"erro": "Credenciais inválidas"}
            )
    return render(request, "login/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
