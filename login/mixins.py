from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

class PermissaoRequiredMixin:
    permissao_necessaria = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if self.permissao_necessaria and not request.user.has_permissao(
            self.permissao_necessaria
        ):
            return render(request, 'paginas/permissao/falha_permissao.html')
        return super().dispatch(request, *args, **kwargs)
