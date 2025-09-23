from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from .models import OrdemServico, Cultura
from .forms import OrdemServicoForm

@login_required
def dashboard(request):
    ordens_ultimas = OrdemServico.objects.filter(owner=request.user).order_by('-data_inicio')[:5] if not request.user.is_superuser else OrdemServico.objects.order_by('-data_inicio')[:5]
    ordens_planejadas = OrdemServico.objects.filter(planejada=True, owner=request.user) if not request.user.is_superuser else OrdemServico.objects.filter(planejada=True)
    lavouras_ativas = Cultura.objects.filter(owner=request.user) if not request.user.is_superuser else Cultura.objects.all()
    produtividade_media = OrdemServico.objects.filter(owner=request.user).aggregate(avg=Avg('produtividade'))['avg'] or 0 if not request.user.is_superuser else OrdemServico.objects.aggregate(avg=Avg('produtividade'))['avg'] or 0
    context = {'ordens_ultimas': ordens_ultimas, 'ordens_planejadas': ordens_planejadas, 'lavouras_ativas': lavouras_ativas, 'produtividade_media': produtividade_media}
    return render(request, 'agricola/dashboard.html', context)

@login_required
def ordens_realizadas(request):
    ordens = OrdemServico.objects.filter(planejada=False, owner=request.user) if not request.user.is_superuser else OrdemServico.objects.filter(planejada=False)
    return render(request, 'agricola/ordens_realizadas.html', {'ordens': ordens})

@login_required
def ordens_planejadas(request):
    ordens = OrdemServico.objects.filter(planejada=True, owner=request.user) if not request.user.is_superuser else OrdemServico.objects.filter(planejada=True)
    return render(request, 'agricola/ordens_planejadas.html', {'ordens': ordens})

@login_required
def lavouras_ativas(request):
    lavouras = Cultura.objects.filter(owner=request.user) if not request.user.is_superuser else Cultura.objects.all()
    return render(request, 'agricola/lavouras_ativas.html', {'lavouras': lavouras})

@login_required
def historico_produtividade(request):
    historico = OrdemServico.objects.filter(owner=request.user).values('cultura__nome').annotate(total=Sum('produtividade')) if not request.user.is_superuser else OrdemServico.objects.values('cultura__nome').annotate(total=Sum('produtividade'))
    return render(request, 'agricola/historico_produtividade.html', {'historico': historico})

@login_required
def lista_ordens(request):
    ordens = OrdemServico.objects.filter(owner=request.user) if not request.user.is_superuser else OrdemServico.objects.all()
    return render(request, 'agricola/lista_ordens.html', {'ordens': ordens})

@login_required
def cria_ordem(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            ordem = form.save(commit=False)
            ordem.owner = request.user
            ordem.save()
            messages.success(request, 'Ordem criada com sucesso.')
            return redirect('lista_ordens')
        else:
            messages.error(request, 'Erro ao criar ordem.')
    else:
        form = OrdemServicoForm()
    return render(request, 'agricola/cria_ordem.html', {'form': form})

@login_required
def aprova_ordem(request, ordem_id):
    ordem = OrdemServico.objects.get(id=ordem_id, owner=request.user) if not request.user.is_superuser else OrdemServico.objects.get(id=ordem_id)
    if request.method == 'POST':
        ordem.aprovado = True
        ordem.save()
        messages.success(request, 'Ordem aprovada.')
        return redirect('lista_ordens')
    return render(request, 'agricola/aprova_ordem.html', {'ordem': ordem})