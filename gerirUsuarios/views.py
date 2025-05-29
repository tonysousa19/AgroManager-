# paginas/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from login.models import User
from .forms import UsuarioForm
from login.mixins import PermissaoRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy


class UsuarioListView(PermissaoRequiredMixin, ListView):
    model = User
    template_name = "paginas/usuarios/listar_usuarios.html"
    context_object_name = "usuarios"
    permissao_necessaria = "gerenciar_usuarios"

    def get_queryset(self):
        queryset = super().get_queryset()
        busca = self.request.GET.get("q", "")
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) | Q(email__icontains=busca)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class UsuarioCreateView(PermissaoRequiredMixin, CreateView):
    model = User
    form_class = UsuarioForm
    template_name = "paginas/usuarios/cadastrar_usuario.html"
    success_url = reverse_lazy("listar_usuarios")
    permissao_necessaria = "cadastrar_usuario"


class UsuarioUpdateView(PermissaoRequiredMixin, UpdateView):
    model = User
    form_class = UsuarioForm
    template_name = "paginas/usuarios/editar_usuario.html"
    success_url = reverse_lazy("listar_usuarios")
    permissao_necessaria = "gerenciar_usuarios"


class UsuarioDeleteView(PermissaoRequiredMixin, DeleteView):
    model = User
    template_name = "paginas/usuarios/excluir_usuario.html"
    success_url = reverse_lazy("listar_usuarios")
    permissao_necessaria = "gerenciar_usuarios"
