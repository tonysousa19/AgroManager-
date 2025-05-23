from django.db import models


class Maquina(models.Model):
    CONDICOES = [
        ("Nova", "Nova"),
        ("Usada", "Usada"),
    ]

    nome = models.CharField(
        verbose_name="Nome", max_length=255, null=False, blank=False
    )
    condicao = models.CharField(
        verbose_name="Condicao", max_length=10, choices=CONDICOES
    )
    ano = models.IntegerField(verbose_name="Ano", null=False, blank=False)
    numero_de_serie = models.CharField(
        verbose_name="Numero de Série",
        max_length=255,
        null=False,
        blank=False,
        default="Sem Serial",
    )

    class Meta:
        ordering = ["-ano"]

    def __str__(self):
        return self.nome


class MaquinaImagem(models.Model):
    maquina = models.ForeignKey(
        Maquina, related_name="imagens", on_delete=models.CASCADE
    )
    imagem = models.ImageField(upload_to="maquinas/imagens/")

    def __str__(self):
        return f"Imagem da máquina {self.maquina.nome}"
