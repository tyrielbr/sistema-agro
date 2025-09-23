from django import forms
from .models import Fazenda, Talhao

class FazendaForm(forms.ModelForm):
    class Meta:
        model = Fazenda
        fields = ['nome', 'localizacao', 'area_total', 'proprietario', 'contrato_arrendamento']

class TalhaoForm(forms.ModelForm):
    class Meta:
        model = Talhao
        fields = ['fazenda', 'nome', 'area', 'coordenadas', 'cultura_atual']