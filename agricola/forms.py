from django import forms
from .models import OrdemServico

from django import forms
from .models import OrdemServico

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['talhao', 'cultura', 'tipo', 'data_inicio', 'data_fim', 'insumos_usados', 'planejada', 'produtividade']