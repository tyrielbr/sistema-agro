from django import forms
from .models import CompraVenda, FornecedorCliente

class CompraVendaForm(forms.ModelForm):
    class Meta:
        model = CompraVenda
        fields = ['tipo', 'fornecedor_cliente', 'data', 'valor', 'produtos', 'centro_custo', 'condicoes_pagamento']

class FornecedorClienteForm(forms.ModelForm):
    class Meta:
        model = FornecedorCliente
        fields = ['nome', 'cpf_cnpj']