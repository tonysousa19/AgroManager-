from django.http import HttpResponseForbidden


def cargo_necessario(*cargos):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.cargo in cargos:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden(
                "Você não tem permissão para acessar esta página."
            )

        return _wrapped_view

    return decorator
