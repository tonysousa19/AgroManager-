from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Maquina, MaquinaImagem
from django.db.models import Q
from .forms import MaquinaForm, MaquinaImagemForm
from login.mixins import PermissaoRequiredMixin



class MaquinaListView(PermissaoRequiredMixin, ListView):
    model = Maquina
    context_object_name = "maquinas"
    template_name = "paginas/maquinas/lista_maquinas.html"
    permissao_necessaria = "cadastrar_maquina" 

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Maquina.objects.filter(Q(name__icontains=query))
        return Maquina.objects.all()


class MaquinaCreateView(PermissaoRequiredMixin, CreateView):
    model = Maquina
    fields = ["nome", "condicao", "ano", "numero_de_serie"]
    template_name = "paginas/maquinas/cadastrar_maquinas.html"
    success_url = reverse_lazy("listar_maquinas")
    permissao_necessaria = "cadastrar_maquina"


    def form_valid(self, form):
        maquina = form.save()

        if "imagens" in self.request.FILES:
            for imagem in self.request.FILES.getlist("imagens"):
                MaquinaImagem.objects.create(maquina=maquina, imagem=imagem)

        return super().form_valid(form)


class MaquinaUpdateView(PermissaoRequiredMixin, UpdateView):
    model = Maquina
    fields = ["nome", "condicao", "ano", "numero_de_serie"]
    template_name = "paginas/maquinas/cadastrar_maquinas.html"
    success_url = reverse_lazy("listar_maquinas")
    permissao_necessaria = "gerenciar_maquinas"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["imagens"] = self.object.imagens.all()
        return context

    def form_valid(self, form):
        maquina = form.save()

        if "imagens" in self.request.FILES:
            for imagem in self.request.FILES.getlist("imagens"):
                MaquinaImagem.objects.create(maquina=maquina, imagem=imagem)

        return super().form_valid(form)
    



class MaquinaDeleteView(PermissaoRequiredMixin, DeleteView):
    model = Maquina
    success_url = reverse_lazy("listar_maquinas")
    template_name = "paginas/maquinas/confirmar_exclusao_maquina.html"
    permissao_necessaria = "gerenciar_maquinas"

