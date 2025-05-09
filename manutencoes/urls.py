from django.urls import path, include
from .views import ManutencaoListView, ManutencaoCreateView, ManutencaoDeleteView, ManutencaoUpdateView

urlpatterns = [
    path("lista-manutencoes/", ManutencaoListView.as_view(), name='lista_manutencoes'),
    path("criar-manutencao/", ManutencaoCreateView.as_view(), name='criar_manutencao'),
    path("editar-manutencao/<int:pk>/", ManutencaoUpdateView.as_view(), name='editar_manutencao'),
    path("deletar-manutencao/<int:pk>/", ManutencaoDeleteView.as_view(), name='deletar_manutencao'),
]
