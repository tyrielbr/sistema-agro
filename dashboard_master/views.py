from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Avg
from fazendas.models import Fazenda
from agricola.models import OrdemServico
from financeiro.models import Vencimento
import json

@staff_member_required
def dashboard(request):
    fazendas = Fazenda.objects.all()
    total_lavouras = OrdemServico.objects.count()
    custos_gerais = Vencimento.objects.aggregate(total=Sum('valor'))['total'] or 0
    produtividade_por_fazenda = OrdemServico.objects.values('talhao__fazenda__nome').annotate(avg=Avg('produtividade'))
    labels = [item['talhao__fazenda__nome'] for item in produtividade_por_fazenda]
    data = [item['avg'] or 0 for item in produtividade_por_fazenda]
    chart_data = json.dumps({'labels': labels, 'data': data})
    context = {'fazendas': fazendas, 'total_lavouras': total_lavouras, 'custos_gerais': custos_gerais, 'chart_data': chart_data}
    return render(request, 'dashboard_master/dashboard.html', context)