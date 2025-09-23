from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Fazenda, Talhao
from .forms import FazendaForm, TalhaoForm
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def lista_fazendas(request):
    fazendas = Fazenda.objects.filter(owner=request.user) if not request.user.is_superuser else Fazenda.objects.all()
    return render(request, 'fazendas/lista_fazendas.html', {'fazendas': fazendas})

@login_required
def cria_fazenda(request):
    if request.method == 'POST':
        form = FazendaForm(request.POST, request.FILES)
        if form.is_valid():
            fazenda = form.save(commit=False)
            fazenda.owner = request.user
            fazenda.save()
            messages.success(request, 'Fazenda criada com sucesso.')
            return redirect('lista_fazendas')
        else:
            messages.error(request, 'Erro ao criar fazenda.')
    else:
        form = FazendaForm()
    return render(request, 'fazendas/cria_fazenda.html', {'form': form})

@login_required
def mapa_talhao(request, talhao_id):
    talhao = Talhao.objects.get(id=talhao_id, owner=request.user) if not request.user.is_superuser else Talhao.objects.get(id=talhao_id)
    context = {'talhao': talhao, 'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY}
    return render(request, 'fazendas/mapa_talhao.html', context)