from django import forms 
from .models import Maquina, ImagemMaquina

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['nome', 'condicao', 'ano', 'numero_de_serie']

class ImagemMaquinaForm(forms.ModelForm):
    class Meta:
        model = ImagemMaquina
        fields = ['imagem']

        def __str__(self):
            return f'Imagem da máquina {self.maquina.nome}'