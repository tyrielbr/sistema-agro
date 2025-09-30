from django import forms
from .models import OrdemServico, Lavoura, Cultura, UsoInsumo

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['talhao', 'cultura', 'tipo', 'data_inicio', 'data_fim', 'volume_agua']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'volume_agua': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'm³'}),
        }

class LavouraForm(forms.ModelForm):
    class Meta:
        model = Lavoura
        fields = ['talhao', 'cultura', 'data_plantio', 'irrigado']
        widgets = {
            'data_plantio': forms.DateInput(attrs={'type': 'date'}),
        }

class CulturaForm(forms.ModelForm):
    class Meta:
        model = Cultura
        fields = ['nome', 'periodo_ideal_inicio', 'periodo_ideal_fim', 'ciclo_min', 'ciclo_max', 'classificacao', 'necessidade_hidrica', 'observacoes']
        widgets = {
            'periodo_ideal_inicio': forms.DateInput(attrs={'type': 'date'}),
            'periodo_ideal_fim': forms.DateInput(attrs={'type': 'date'}),
            'ciclo_min': forms.NumberInput(attrs={'min': 90, 'max': 120}),
            'ciclo_max': forms.NumberInput(attrs={'min': 90, 'max': 120}),
            'necessidade_hidrica': forms.NumberInput(attrs={'step': '0.01'}),
        }

class UsoInsumoForm(forms.ModelForm):
    class Meta:
        model = UsoInsumo
        fields = ['insumo', 'quantidade', 'receita_por_ha', 'unidade_medida']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'step': '0.01'}),
            'receita_por_ha': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'ex: 200 ml/ha'}),
            'unidade_medida': forms.Select(choices=[('ml/ha', 'ml/ha'), ('kg/ha', 'kg/ha'), ('l/ha', 'l/ha'), ('g/ha', 'g/ha')]),
        }