# login/utils.py
from functools import wraps
from django.http import HttpResponseForbidden


def permissao_necessaria(nome_permissao):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Você precisa estar logado.")
            if not request.user.has_permissao(nome_permissao):
                return HttpResponseForbidden("Você não tem permissão.")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
