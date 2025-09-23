from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Equipamento, Maquina, Manutencao, Abastecimento
from .forms import EquipamentoForm, AbastecimentoForm

@login_required
def dashboard(request):
    equipamentos = Equipamento.objects.filter(owner=request.user) if not request.user.is_superuser else Equipamento.objects.all()
    ordens = Manutencao.objects.filter(owner=request.user) if not request.user.is_superuser else Manutencao.objects.all()
    alertas = []  # Simples: se horas > 500, alerta troca óleo
    for eq in equipamentos:
        if eq.horas_registradas > 500:
            alertas.append(f"Alerta: Troca de óleo para {eq.nome} (horas: {eq.horas_registradas})")
        if eq.horas_registradas > 1000:
            alertas.append(f"Alerta: Troca de filtro para {eq.nome}")
    context = {'equipamentos': equipamentos, 'ordens': ordens, 'alertas': alertas}
    return render(request, 'maquinas/dashboard.html', context)

@login_required
def cria_abastecimento(request):
    if request.method == 'POST':
        form = AbastecimentoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            messages.success(request, 'Abastecimento registrado.')
            return redirect('maquinas_dashboard')
    else:
        form = AbastecimentoForm()
    return render(request, 'maquinas/cria_abastecimento.html', {'form': form})

@login_required
def cria_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            messages.success(request, 'Equipamento cadastrado.')
            return redirect('maquinas_dashboard')
    else:
        form = EquipamentoForm()
    return render(request, 'maquinas/cria_equipamento.html', {'form': form})