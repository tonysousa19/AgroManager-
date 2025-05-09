from django.contrib import admin
from django.urls import path
from .views import MaquinaListView, MaquinaCreateView, MaquinaUpdateView, MaquinaDeleteView

urlpatterns = [
    path("lista-maquinas/", MaquinaListView.as_view(), name='lista_maquinas'),
    path("criar-maquina/", MaquinaCreateView.as_view(), name='criar_maquina'),
    path("editar-maquina/", MaquinaUpdateView.as_view(), name='editar_maquina'),
    path("deletar-maquina/", MaquinaDeleteView.as_view(), name='deletar_maquina'),


]
