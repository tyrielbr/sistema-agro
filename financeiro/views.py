from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import timedelta, date
from .models import Vencimento, Contrato, Financiamento, ContaAgro
from .forms import VencimentoForm, ContratoForm, FinanciamentoForm
from django.db.models import Sum

@login_required
def dashboard(request):
    entradas = Vencimento.objects.filter(
        conta__account__balance_type='credit', quitado=True, owner=request.user
    ).aggregate(total=Sum('valor'))['total'] or 0 if not request.user.is_superuser else Vencimento.objects.filter(
        conta__account__balance_type='credit', quitado=True
    ).aggregate(total=Sum('valor'))['total'] or 0
    saidas = Vencimento.objects.filter(
        conta__account__balance_type='debit', quitado=True, owner=request.user
    ).aggregate(total=Sum('valor'))['total'] or 0 if not request.user.is_superuser else Vencimento.objects.filter(
        conta__account__balance_type='debit', quitado=True
    ).aggregate(total=Sum('valor'))['total'] or 0
    fluxo = entradas - saidas
    context = {'fluxo': fluxo}
    return render(request, 'financeiro/dashboard.html', context)

@login_required
def vencimentos(request):
    periodo = request.GET.get('periodo', 'diario')
    hoje = date.today()
    if periodo == 'diario':
        filtro = Q(data_vencimento=hoje)
    elif periodo == 'semanal':
        filtro = Q(data_vencimento__gte=hoje, data_vencimento__lte=hoje + timedelta(days=7))
    elif periodo == 'mensal':
        filtro = Q(data_vencimento__month=hoje.month, data_vencimento__year=hoje.year)
    vencimentos = Vencimento.objects.filter(filtro, owner=request.user) if not request.user.is_superuser else Vencimento.objects.filter(filtro)
    return render(request, 'financeiro/vencimentos.html', {'vencimentos': vencimentos, 'periodo': periodo})

@login_required
def cria_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            messages.success(request, 'Contrato cadastrado.')
            return redirect('financeiro_dashboard')
    else:
        form = ContratoForm()
    return render(request, 'financeiro/cria_contrato.html', {'form': form})

@login_required
def cria_financiamento(request):
    if request.method == 'POST':
        form = FinanciamentoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            form.save_m2m()  # Para salvar vencimentos (ManyToMany)
            messages.success(request, 'Financiamento cadastrado.')
            return redirect('financeiro_dashboard')
    else:
        form = FinanciamentoForm()
    return render(request, 'financeiro/cria_financiamento.html', {'form': form})