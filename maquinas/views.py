from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Maquina, MaquinaImagem
from django.db.models import Q
from .forms import MaquinaForm, MaquinaImagemForm


class MaquinaListView(ListView):
    model = Maquina
    context_object_name = "maquinas"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Maquina.objects.filter(Q(name__icontains=query))
        return Maquina.objects.all()


class MaquinaCreateView(CreateView):
    model = Maquina
    fields = ["nome", "condicao", "ano", "numero_de_serie"]
    template_name = "maquinas/maquina_form.html"
    success_url = reverse_lazy("listar_maquinas")

    def form_valid(self, form):
        maquina = form.save()

        if "imagens" in self.request.FILES:
            for imagem in self.request.FILES.getlist("imagens"):
                MaquinaImagem.objects.create(maquina=maquina, imagem=imagem)

        return super().form_valid(form)


class MaquinaUpdateView(UpdateView):
    model = Maquina
    fields = ["nome", "condicao", "ano", "numero_de_serie"]
    template_name = "maquinas/maquina_form.html"
    success_url = reverse_lazy("listar_maquinas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["imagens"] = self.object.images.all()
        return context

    def form_valid(self, form):
        maquina = form.save()

        if "images" in self.request.FILES:
            for imagem in self.request.FILES.getlist("imagens"):
                MaquinaImagem.objects.create(maquina=maquina, imagem=imagem)

        return super().form_valid(form)


class MaquinaDeleteView(DeleteView):
    model = Maquina
    success_url = reverse_lazy("listar_maquinas")
