# login/mixins.py
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden


class PermissaoRequiredMixin:
    permissao_necessaria = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())  # redireciona para login
        if self.permissao_necessaria and not request.user.has_permissao(
            self.permissao_necessaria
        ):
            return HttpResponseForbidden("Você não tem permissão.")
        return super().dispatch(request, *args, **kwargs)
