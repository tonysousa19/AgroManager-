from django.db import models
from maquinas.models import Maquina


class Manutencao(models.Model):
    maquina = models.ForeignKey(
        Maquina,
        on_delete=models.CASCADE,
        related_name="manutencoes",
        blank=False,
        null=False,
    )
    data = models.DateField(verbose_name="Data da Manutenção")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=False)
    pecas_usadas = models.CharField(
        verbose_name="Peças Utilizadas", max_length=255, blank=True
    )
    custo = models.DecimalField(
        verbose_name="Custo Total (R$)", max_digits=10, decimal_places=2, default=0
    )

    class Meta:
        ordering = ["-data"]

    def __str__(self):
        return f"{self.maquina.nome} - {self.data}"
