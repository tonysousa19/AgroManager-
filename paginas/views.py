from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseForbidden


@login_required
def pagina_inicial(request):
    return render(request, "paginas/home.html")

