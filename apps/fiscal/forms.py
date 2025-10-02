from django import forms
from .models import NfRecebida, ItemNf, LancamentoEstoque
from django.core.exceptions import ValidationError

class NfRecebidaForm(forms.ModelForm):
    class Meta:
        model = NfRecebida
        fields = ['status', 'motivo_rejeicao']  # Apenas para edição de status/motivo

class ItemNfForm(forms.ModelForm):
    class Meta:
        model = ItemNf
        fields = ['produto', 'ncm', 'quantidade', 'valor_unitario']

class LancamentoEstoqueForm(forms.ModelForm):
    class Meta:
        model = LancamentoEstoque
        fields = ['quantidade_confirmada', 'lote']

    def clean_quantidade_confirmada(self):
        quantidade = self.cleaned_data['quantidade_confirmada']
        if quantidade <= 0:
            raise ValidationError('Quantidade deve ser maior que zero.')
        return quantidade