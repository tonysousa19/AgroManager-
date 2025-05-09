from django.urls import path, include
from .views import (
    MaquinaCreateView,
    MaquinaListView,
    MaquinaDeleteView,
    MaquinaUpdateView,
)

urlpatterns = [
    path("criar-maquinas/", MaquinaCreateView.as_view(), name="criar_maquinas"),
    path("lista-maquinas/", MaquinaListView.as_view(), name="listar_maquinas"),
    path(
        "deletar-maquinas/<int:pk>/",
        MaquinaDeleteView.as_view(),
        name="deletar_maquinas",
    ),
    path(
        "editar-maquinas//<int:pk>", MaquinaUpdateView.as_view(), name="editar_maquinas"
    ),
]
