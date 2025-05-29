from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login.models import User
from maquinas.models import Maquina 
from manutencoes.models import Manutencao 
from django.http import HttpResponseForbidden

@login_required
def dashboard_view(request):
    if not request.user.has_permissao("ver_dashboard"):
        return render(request, 'paginas/permissao/falha_permissao.html')
    
    total_usuarios = User.objects.count()
    total_maquinas = Maquina.objects.count()
    total_manutencoes = Manutencao.objects.count()
    

    context = {
        'total_usuarios': total_usuarios,
        'total_maquinas': total_maquinas,
        'total_manutencoes': total_manutencoes,
    }

    return render(request, 'paginas/dashboard/dashboard.html', context)
