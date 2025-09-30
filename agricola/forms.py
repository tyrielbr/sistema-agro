from django import forms
from django.forms import inlineformset_factory
from .models import OrdemServico, Lavoura, Cultura, UsoInsumo

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['titulo', 'observacoes', 'anexo', 'talhao', 'cultura', 'tipo', 'data_inicio', 'data_fim', 'volume_agua']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
            'anexo': forms.FileInput(attrs={'class': 'form-control-file', 'accept': '.pdf,.jpg,.png'}),
            'talhao': forms.Select(attrs={'class': 'form-control'}),
            'cultura': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'volume_agua': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'm³', 'class': 'form-control'}),
        }

class UsoInsumoForm(forms.ModelForm):
    class Meta:
        model = UsoInsumo
        fields = ['insumo', 'receita_por_ha', 'unidade_medida', 'quantidade']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-control'}),
            'receita_por_ha': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'ex: 200 ml/ha', 'class': 'form-control'}),
            'unidade_medida': forms.Select(attrs={'class': 'form-control'}, choices=[('ml/ha', 'ml/ha'), ('kg/ha', 'kg/ha'), ('l/ha', 'l/ha'), ('g/ha', 'g/ha')]),
            'quantidade': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }

UsoInsumoFormSet = inlineformset_factory(OrdemServico, UsoInsumo, form=UsoInsumoForm, extra=1, can_delete=True)

class LavouraForm(forms.ModelForm):
    class Meta:
        model = Lavoura
        fields = ['talhao', 'cultura', 'data_plantio', 'irrigado']
        widgets = {
            'data_plantio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'talhao': forms.Select(attrs={'class': 'form-control'}),
            'cultura': forms.Select(attrs={'class': 'form-control'}),
            'irrigado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CulturaForm(forms.ModelForm):
    class Meta:
        model = Cultura
        fields = ['nome', 'periodo_ideal_inicio', 'periodo_ideal_fim', 'ciclo_min', 'ciclo_max', 'classificacao', 'necessidade_hidrica', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'periodo_ideal_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'periodo_ideal_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ciclo_min': forms.NumberInput(attrs={'min': 90, 'max': 120, 'class': 'form-control'}),
            'ciclo_max': forms.NumberInput(attrs={'min': 90, 'max': 120, 'class': 'form-control'}),
            'classificacao': forms.Select(attrs={'class': 'form-control'}),
            'necessidade_hidrica': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }