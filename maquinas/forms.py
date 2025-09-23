from django import forms
from .models import Abastecimento, Equipamento

class AbastecimentoForm(forms.ModelForm):
    class Meta:
        model = Abastecimento
        fields = ['equipamento', 'produto', 'quantidade_litros', 'horimetro', 'data_abastecimento']

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'marca', 'ano', 'horas_registradas', 'km_registrados', 'nota_fiscal']