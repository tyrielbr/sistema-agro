from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from .models import OrdemServico, Cultura, Lavoura
from .forms import OrdemServicoForm, LavouraForm, CulturaForm, UsoInsumoFormSet

@login_required
def dashboard(request):
    user_filter = {'owner': request.user} if not request.user.is_superuser else {}
    
    ordens_ultimas = OrdemServico.objects.filter(**user_filter).order_by('-data_inicio')[:5]
    ordens_planejadas = OrdemServico.objects.filter(planejada=True, **user_filter)
    lavouras_ativas = Lavoura.objects.filter(owner=request.user) if not request.user.is_superuser else Lavoura.objects.all()
    produtividade_media = OrdemServico.objects.filter(**user_filter).aggregate(avg=Avg('produtividade'))['avg'] or 0
    ordens_pendentes = OrdemServico.objects.filter(aprovado=False, data_fim__isnull=True, **user_filter)

    context = {
        'ordens_ultimas': ordens_ultimas,
        'ordens_planejadas': ordens_planejadas,
        'lavouras_ativas': lavouras_ativas,
        'produtividade_media': produtividade_media,
        'ordens_pendentes': ordens_pendentes,
    }
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
    lavouras = Lavoura.objects.filter(owner=request.user) if not request.user.is_superuser else Lavoura.objects.all()
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
        form = OrdemServicoForm(request.POST, request.FILES)
        formset = UsoInsumoFormSet(request.POST, instance=OrdemServico())
        if form.is_valid() and formset.is_valid():
            ordem = form.save(commit=False)
            ordem.owner = request.user
            ordem.save()
            formset.instance = ordem
            formset.save()
            messages.success(request, 'Ordem criada com sucesso.')
            return redirect('lista_ordens')
        else:
            messages.error(request, 'Erro ao criar ordem.')
    else:
        form = OrdemServicoForm()
        formset = UsoInsumoFormSet(instance=OrdemServico())
    return render(request, 'agricola/cria_ordem.html', {'form': form, 'formset': formset})

@login_required
def aprova_ordem(request, ordem_id):
    ordem = OrdemServico.objects.get(id=ordem_id, owner=request.user) if not request.user.is_superuser else OrdemServico.objects.get(id=ordem_id)
    if request.method == 'POST':
        ordem.aprovado = True
        ordem.save()
        messages.success(request, 'Ordem aprovada.')
        return redirect('lista_ordens')
    return render(request, 'agricola/aprova_ordem.html', {'ordem': ordem})

@login_required
def cria_lavoura(request):
    if request.method == 'POST':
        form = LavouraForm(request.POST)
        if form.is_valid():
            lavoura = form.save(commit=False)
            lavoura.owner = request.user
            lavoura.save()
            messages.success(request, 'Lavoura criada com sucesso!')
            return redirect('lista_lavouras')
        else:
            messages.error(request, 'Erro ao criar lavoura: ' + str(form.errors))
    else:
        form = LavouraForm()
    return render(request, 'agricola/cria_lavoura.html', {'form': form})
    
def lista_lavouras(request):
    lavouras = Lavoura.objects.filter(ativo=True)
    return render(request, 'agricola/lista_lavouras.html', {'lavouras': lavouras})

def remove_lavoura(request, lavoura_id):
    lavoura = get_object_or_404(Lavoura, id=lavoura_id)
    if request.method == 'POST':
        lavoura.ativo = False  # Soft delete
        lavoura.save()
        messages.success(request, 'Lavoura removida com sucesso!')
        return redirect('lista_lavouras')
    return render(request, 'agricola/remove_lavoura.html', {'lavoura': lavoura})

@login_required
def gerenciar_culturas(request):
    if request.method == 'POST':
        form = CulturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cultura criada com sucesso!')
            return redirect('gerenciar_culturas')
    else:
        form = CulturaForm()
    culturas = Cultura.objects.all()
    return render(request, 'agricola/gerenciar_culturas.html', {'form': form, 'culturas': culturas})