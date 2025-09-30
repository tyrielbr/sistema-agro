from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CentroCusto, Funcionario
from .forms import FuncionarioForm
from maquinas.models import Manutencao
from django.db import models  # Added this import for models.Sum

@login_required
def dashboard(request):
    centros = CentroCusto.objects.filter(owner=request.user) if not request.user.is_superuser else CentroCusto.objects.all()
    custos_maquinas = Manutencao.objects.filter(owner=request.user).aggregate(total=models.Sum('custo'))['total'] or 0 if not request.user.is_superuser else Manutencao.objects.aggregate(total=models.Sum('custo'))['total'] or 0
    custos_pessoal = Funcionario.objects.filter(owner=request.user).aggregate(total=models.Sum('salario_efetivo'))['total'] or 0 if not request.user.is_superuser else Funcionario.objects.aggregate(total=models.Sum('salario_efetivo'))['total'] or 0
    context = {'centros': centros, 'custos_maquinas': custos_maquinas, 'custos_pessoal': custos_pessoal}
    return render(request, 'administrativo/dashboard.html', context)

@login_required
def cria_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save(commit=False)
            funcionario.owner = request.user
            funcionario.save()
            messages.success(request, 'Funcionário cadastrado.')
            return redirect('administrativo_dashboard')
        else:
            messages.error(request, 'Erro no formulário.')
    else:
        form = FuncionarioForm()
    return render(request, 'administrativo/cria_funcionario.html', {'form': form})

@login_required
def lista_funcionarios(request):
    funcionarios = Funcionario.objects.filter(owner=request.user) if not request.user.is_superuser else Funcionario.objects.all()
    return render(request, 'administrativo/lista_funcionarios.html', {'funcionarios': funcionarios})