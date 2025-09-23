from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import CompraVenda, FornecedorCliente
from .forms import CompraVendaForm, FornecedorClienteForm
from estoque.models import Produto

@login_required
def dashboard(request):
    compras = CompraVenda.objects.filter(tipo='compra', owner=request.user).aggregate(total=Sum('valor'))['total'] or 0 if not request.user.is_superuser else CompraVenda.objects.filter(tipo='compra').aggregate(total=Sum('valor'))['total'] or 0
    vendas = CompraVenda.objects.filter(tipo='venda', owner=request.user).aggregate(total=Sum('valor'))['total'] or 0 if not request.user.is_superuser else CompraVenda.objects.filter(tipo='venda').aggregate(total=Sum('valor'))['total'] or 0
    estoque_disponivel = Produto.objects.filter(owner=request.user).aggregate(total=Sum('quantidade'))['total'] or 0 if not request.user.is_superuser else Produto.objects.aggregate(total=Sum('quantidade'))['total'] or 0
    estimativa_vendas = vendas * 1.1  # Simples projeção +10%
    context = {'compras': compras, 'vendas': vendas, 'estoque_disponivel': estoque_disponivel, 'estimativa_vendas': estimativa_vendas}
    return render(request, 'comercial/dashboard.html', context)

@login_required
def cria_compra_venda(request):
    if request.method == 'POST':
        form = CompraVendaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            form.save_m2m()
            messages.success(request, 'Transação cadastrada.')
            return redirect('comercial_dashboard')
    else:
        form = CompraVendaForm()
    return render(request, 'comercial/cria_compra_venda.html', {'form': form})

@login_required
def cria_fornecedor_cliente(request):
    if request.method == 'POST':
        form = FornecedorClienteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            messages.success(request, 'Fornecedor/Cliente cadastrado.')
            return redirect('comercial_dashboard')
    else:
        form = FornecedorClienteForm()
    return render(request, 'comercial/cria_fornecedor_cliente.html', {'form': form})