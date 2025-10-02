from django import forms
from .models import Vencimento, Contrato, Financiamento, ContaAgro

class VencimentoForm(forms.ModelForm):
    class Meta:
        model = Vencimento
        fields = ['conta', 'data_vencimento', 'valor', 'quitado', 'anexo']
        widgets = {
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}),
        }

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['tipo', 'descricao', 'valor', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class FinanciamentoForm(forms.ModelForm):
    class Meta:
        model = Financiamento
        fields = ['descricao', 'valor', 'data', 'vencimentos']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }