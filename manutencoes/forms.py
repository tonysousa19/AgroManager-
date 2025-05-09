from django import forms
from .models import Manutencao
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['maquina', 'data', 'descricao', 'pecas_usadas', 'custo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar', css_class='btn btn-success'))
