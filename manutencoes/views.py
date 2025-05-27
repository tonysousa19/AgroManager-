from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from .models import Manutencao


class ManutencaoListView(ListView):
    model = Manutencao
    context_object_name = "manutencoes"
    template_name = "paginas/manutencoes/manutencao_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        data_inicio = self.request.GET.get("data_inicio")
        data_fim = self.request.GET.get("data_fim")

        if search:
            queryset = queryset.filter(descricao__icontains=search)

        if data_inicio:
            queryset = queryset.filter(data__gte=parse_date(data_inicio))
        if data_fim:
            queryset = queryset.filter(data__lte=parse_date(data_fim))

        return queryset


class ManutencaoCreateView(CreateView):
    model = Manutencao
    fields = ["maquina", "data", "descricao", "pecas_usadas", "custo"]
    template_name = "paginas/manutencoes/manutencao_form.html"
    success_url = reverse_lazy("listar_manutencoes")


class ManutencaoUpdateView(UpdateView):
    model = Manutencao
    fields = ["maquina", "data", "descricao", "pecas_usadas", "custo"]
    template_name = "paginas/manutencoes/manutencao_form.html"
    success_url = reverse_lazy("listar_manutencoes")


class ManutencaoDeleteView(DeleteView):
    model = Manutencao
    success_url = reverse_lazy("listar_manutencoes")
    template_name = "paginas/manutencoes/manutencao_confirm_delete.html"
