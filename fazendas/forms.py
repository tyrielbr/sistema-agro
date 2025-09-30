from django import forms
from django.core.exceptions import ValidationError
from .models import Pessoa, Fazenda, Arrendamento, Area, Talhao

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'cpf_cnpj', 'tipo', 'poder_decisao']

class FazendaForm(forms.ModelForm):
    class Meta:
        model = Fazenda
        fields = ['nome', 'localizacao', 'area_total', 'proprietarios_socios']

    def clean_proprietarios_socios(self):
        proprietarios = self.cleaned_data['proprietarios_socios']
        if not proprietarios:
            raise ValidationError('Selecione pelo menos um proprietário ou sócio.')
        return proprietarios

class ArrendamentoForm(forms.ModelForm):
    class Meta:
        model = Arrendamento
        fields = ['nome', 'localizacao', 'area_total', 'proprietarios_socios', 'contrato']

    def clean_proprietarios_socios(self):
        proprietarios = self.cleaned_data['proprietarios_socios']
        if not proprietarios:
            raise ValidationError('Selecione pelo menos um proprietário ou sócio.')
        return proprietarios

    def clean_contrato(self):
        contrato = self.cleaned_data['contrato']
        if not contrato:
            raise ValidationError('Um contrato é obrigatório para arrendamentos.')
        return contrato

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nome', 'fazenda', 'arrendamento', 'area', 'latitude', 'longitude', 'kmz_file']

    def clean(self):
        cleaned_data = super().clean()
        fazenda = cleaned_data.get('fazenda')
        arrendamento = cleaned_data.get('arrendamento')
        if fazenda and arrendamento:
            raise ValidationError('Uma área não pode pertencer a uma fazenda e um arrendamento ao mesmo tempo.')
        if not fazenda and not arrendamento:
            raise ValidationError('Uma área deve pertencer a uma fazenda ou arrendamento.')
        return cleaned_data

class TalhaoForm(forms.ModelForm):
    class Meta:
        model = Talhao
        fields = ['nome', 'area', 'area_size', 'latitude', 'longitude', 'kmz_file']
    def __init__(self, *args, area_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if area_id is not None:
            self.fields['fazenda'].queryset = self.fields['fazenda'].queryset.filter(area__id=area_id)
            # Ou seta um valor inicial, se for um campo direto
            # self.initial['fazenda'] = area_id  # Descomenta se fazenda for o campo certo