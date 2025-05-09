from django import forms
from .models import Maquina, MaquinaImagem


class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ["nome", "condicao", "ano", "numero_de_serie"]


class MaquinaImagemForm(forms.ModelForm):
    class Meta:
        model = MaquinaImagem
        fields = ["imagem"]

        def __str__(self):
            return f"Imagem da máquina {self.maquina.nome}"
