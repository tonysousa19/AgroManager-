from django.urls import path
from . import views

urlpatterns = [
    # Paginas de login
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Home
    path("", views.login_view, name="login"),
    path("home/", views.home, name="home"),
    # Paginas de permissao
]
