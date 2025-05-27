from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class Permissao(models.Model):
    nome = models.CharField(max_length=100)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Permissão"
        verbose_name_plural = "Permissões"


class Cargo(models.Model):
    nome = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    permissoes = models.ManyToManyField(Permissao, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"


ROLES = [
    ("adm", "Administrador"),
    ("gestor", "Gestor"),
    ("func", "Funcionário"),
]


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.create_user(email, password, **extra_fields)

        if not user.cargo:
            cargo_adm, _ = Cargo.objects.get_or_create(nome="Administrador")
            user.cargo = cargo_adm
            user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def has_permissao(self, nome_permissao):
        if self.cargo:
            return self.cargo.permissoes.filter(nome=nome_permissao).exists()
        return False

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome"]

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
