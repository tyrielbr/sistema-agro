from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'data_nascimento', 'cpf', 'rg', 'telefone', 'endereco', 'condicao', 'salario_registrado', 'salario_efetivo', 'valor_hora_extra', 'valor_diaria_extra']
        widgets = {
            'nome': forms.TextInput(attrs={'required': True}),
            'data_nascimento': forms.DateInput(attrs={'required': True}),
            'cpf': forms.TextInput(attrs={'required': True}),
        }