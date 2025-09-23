from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from fazendas.models import Fazenda
from agricola.models import OrdemServico
from financeiro.models import Vencimento
from django.db.models import Sum, Avg
import json

@staff_member_required
def dashboard(request):
    fazendas = Fazenda.objects.all()
    total_lavouras = OrdemServico.objects.count()
    custos_gerais = Vencimento.objects.aggregate(total=Sum('valor'))['total'] or 0
    produtividade_por_fazenda = OrdemServico.objects.values('talhao__fazenda__nome').annotate(avg=Avg('produtividade'))
    # Dados para gráficos (JSON para Chart.js)
    labels = [item['talhao__fazenda__nome'] for item in produtividade_por_fazenda]
    data = [item['avg'] for item in produtividade_por_fazenda]
    chart_data = json.dumps({'labels': labels, 'data': data})
    context = {'fazendas': fazendas, 'total_lavouras': total_lavouras, 'custos_gerais': custos_gerais, 'chart_data': chart_data}
    return render(request, 'dashboard_master/dashboard.html', context)