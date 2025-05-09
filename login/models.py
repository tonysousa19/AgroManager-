from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

ROLES = [
    ("adm", "Administrador"),
    ("gestor", "Gestor"),
    ("func", "Funcionário"),
]


# Classe personalziada para gerenciar o usuário:
# A classe UserManager herda da classe BaseUserManagere implementa os métodos create_user e create_superuser
class UserManager(BaseUserManager):

    # Método para criar o usuário
    # O usuário é criado com o email e a senha fornecidos
    # O usuário é criado com o método normalize_email, que normaliza o email para o formato correto
    # O usuário é criado com o método set_password, que define a senha do usuário
    # O usuário é criado com o método save, que salva o usuário no banco de dados

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    # Método para criar o superusuário
    # O superusuário é um usuário com permissões administrativas
    # O superusuário é criado com o cargo 'adm' e as permissões is_staff e is_superuser definidas como True
    # O superusuário é criado com o método create_user, mas com os campos is_staff e is_superuser definidos como True

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("cargo", "adm")
        return self.create_user(email, password, **extra_fields)


# Classe personalizada para o usuário:
# A classe User herda da classe AbstractBaseUser e PermissionsMixin
# A classe User tem os campos email, nome, cargo, is_active e is_staff
# O campo email é o campo de login do usuário e é único
# O campo nome é o nome do usuário
# O campo cargo é o cargo do usuário e tem as opções 'adm', 'gestor' e 'func'
# O campo is_active é um booleano que indica se o usuário está ativo ou não
# O campo is_staff é um booleano que indica se o usuário é um membro da equipe de administração ou não
# A classe User tem um gerenciador de usuários personalizado, que é a classe UserManager
class User(AbstractBaseUser, PermissionsMixin):
    # Definindo os campos do usuário
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    cargo = models.CharField(max_length=10, choices=ROLES, default="func")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Definindo o gerenciador de usuários personalizado
    # O gerenciador de usuários personalizado é a classe UserManager
    objects = UserManager()

    # Definindo o campo de login do usuário
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "cargo"]

    def __str__(self):
        return self.nome
