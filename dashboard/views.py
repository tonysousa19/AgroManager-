from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login.models import User
from maquinas.models import Maquina  # ou MáquinaAgrícola, depende do seu nome real
from manutencoes.models import Manutencao  # ajuste o nome se for diferente
from django.http import HttpResponseForbidden

@login_required
def dashboard_view(request):
    if not request.user.has_permissao("ver_dashboard"):
        return HttpResponseForbidden("Você não tem permissão para acessar o dashboard.")
    
    total_usuarios = User.objects.count()
    total_maquinas = Maquina.objects.count()
    total_manutencoes = Manutencao.objects.count()
    

    context = {
        'total_usuarios': total_usuarios,
        'total_maquinas': total_maquinas,
        'total_manutencoes': total_manutencoes,
    }

    return render(request, 'paginas/dashboard/dashboard.html', context)
