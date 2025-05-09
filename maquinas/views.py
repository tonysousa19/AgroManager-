from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Maquina, ImagemMaquina
from django.db.models import Q
from .forms import MaquinaForm
from login.decorators import cargo_necessario
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
@method_decorator(cargo_necessario("adm"), name='dispatch')
class MaquinaListView(ListView):
    model = Maquina
    context_object_name = 'maquinas'

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        if query:
            return Maquina.objects.filter(Q(name__icontains=query)) 
        
        return Maquina.objects.all()

@method_decorator(login_required, name='dispatch')
@method_decorator(cargo_necessario("adm"), name='dispatch')
class MaquinaCreateView(CreateView):
    model =  Maquina
    fields = ['nome', 'condicao', 'ano', 'numero_de_serie']
    template_name = 'maquinas/maquina_form.html'
    success_url = reverse_lazy('lista_maquinas')


    def form_valid(self, form):
        maquina = form.save()

        if 'imagens' in self.request.FILES:
            for imagem in self.request.FILES.getlist('imagens'):
                Maquina.objects.create(maquina=maquina, imagem=imagem)

        return super().form_valid(form)
    

class MaquinaUpdateView(UpdateView):
    model = Maquina
    fields = ['nome', 'condicao', 'ano', 'serial_number']
    template_name = 'maquinas/maquina_form.html'     
    success_url = reverse_lazy('lista_maquinas')

    def form_valid(self, form):
        maquina = form.save()

        if 'imagens' in self.request.FILES:
            for imagem in self.request.FILES.getlist('imagens'):
                Maquina.objects.create(maquina=maquina, imagem=imagem)

        return super().form_valid(form)
    

class MaquinaDeleteView(DeleteView):
    model = Maquina
    success_url = reverse_lazy('lista_maquinas')
    
     



