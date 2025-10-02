from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'data_nascimento', 'cpf', 'rg', 'telefone', 'endereco', 'condicao', 'salario_registrado', 'salario_efetivo', 'valor_hora_extra', 'valor_diaria_extra']