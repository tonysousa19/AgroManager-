from django.urls import path
from paginas.views import pagina_inicial
from dashboard.views import dashboard_view
from relatorios.views import relatorio_maquinas_manutencoes, pagina_relatorio
from gerirUsuarios.views import UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView
from maquinas.views import MaquinaListView, MaquinaCreateView, MaquinaUpdateView, MaquinaDeleteView
from manutencoes.views import ManutencaoListView, ManutencaoCreateView, ManutencaoDeleteView, ManutencaoUpdateView

urlpatterns = [
    #Pagina inicial 
    path("", pagina_inicial, name="pagina_inicial"),
    
    # Usuarios
    path("listar-usuarios/", UsuarioListView.as_view(), name="listar_usuarios"),
    path("cadastrar-usuarios/", UsuarioCreateView.as_view(), name="cadastrar_usuario"),
    path("editar-usuario/<int:pk>/", UsuarioUpdateView.as_view(), name="editar_usuario"),
    path("excluir-usuario/<int:pk>/", UsuarioDeleteView.as_view(), name="excluir_usuario"),

    # Maquinas
    path("listar-maquinas/", MaquinaListView.as_view(), name="listar_maquinas"),
    path("cadastrar-maquinas/", MaquinaCreateView.as_view(), name="cadastrar_maquinas"),
    path("editar-maquina/<int:pk>/", MaquinaUpdateView.as_view(), name="editar_maquinas"),
    path("excluir-maquina/<int:pk>/",MaquinaDeleteView.as_view(), name="excluir_maquinas"),

    # Manutencoes
    path("lista-manutencoes/", ManutencaoListView.as_view(), name="listar_manutencoes"),
    path("criar-manutencao/", ManutencaoCreateView.as_view(), name="criar_manutencoes"),
    path("editar-manutencao/<int:pk>/", ManutencaoUpdateView.as_view(), name="editar_manutencao"),
    path("deletar-manutencao/<int:pk>/",ManutencaoDeleteView.as_view(),name="deletar_manutencao"),

    #Dashboards
    path("dashboard/", dashboard_view, name="ver_dashboard"),

    #Relatorios
    path("relatorios/", pagina_relatorio, name="relatorios_manutencoes"),
    path("relatorios/gerar_relatorio", relatorio_maquinas_manutencoes, name="gerar_relatorios_manutencoes"),

]
