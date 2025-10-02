
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from django.utils import timezone
from .models import NfRecebida, ItemNf, LancamentoEstoque
from .forms import NfRecebidaForm, ItemNfForm, LancamentoEstoqueForm
from .utils import load_certificate
from .tasks import download_nf_diaria
from apps.estoque.models import EstoqueMovimento
from apps.financeiro.models import Titulo
import xml.etree.ElementTree as ET

@login_required
def dashboard(request):
    nf_list = NfRecebida.objects.filter(user=request.user).order_by('-data_emissao')[:20]
    context = {'nf_list': nf_list}
    return render(request, 'fiscal/nf_recebidas.html', context)

@login_required
def detalhes_nf(request, pk):
    try:
        nf = get_object_or_404(NfRecebida, pk=pk, user=request.user)
        itens = nf.itens.all()
        if request.method == 'POST':
            form = NfRecebidaForm(request.POST, instance=nf)
            if form.is_valid():
                nf = form.save()
                if nf.status == 'ciencia':
                    messages.info(request, 'NF-e marcada como ciência.')
                elif nf.status == 'rejeitada':
                    messages.warning(request, 'NF-e rejeitada.')
                elif nf.status == 'pendente processamento':
                    messages.info(request, 'NF-e marcada para processamento.')
                return redirect('fiscal_dashboard')
            else:
                messages.error(request, 'Erro ao processar ação.')
        else:
            form = NfRecebidaForm(instance=nf)
        context = {'nf': nf, 'itens': itens, 'form': form}
        return render(request, 'fiscal/detalhes_nf.html', context)
    except NfRecebida.DoesNotExist:
        messages.error(request, 'NF-e não encontrada.')
        return redirect('fiscal_dashboard')

@login_required
def lancamento_nf(request, pk):
    try:
        nf = get_object_or_404(NfRecebida, pk=pk, user=request.user, status='pendente processamento')
        itens = nf.itens.all()
        if not itens:
            messages.error(request, 'Nenhum item associado à NF-e.')
            return redirect('fiscal_dashboard')
        if request.method == 'POST':
            for item in itens:
                lancamento = LancamentoEstoque(item=item, user=request.user, nf_recebida=nf)
                lancamento_form = LancamentoEstoqueForm(request.POST, instance=lancamento)
                if lancamento_form.is_valid():
                    lancamento = lancamento_form.save()
                    EstoqueMovimento.objects.create(
                        produto_id=item.produto,  # Adjust if produto is ForeignKey
                        quantidade=lancamento.quantidade_confirmada,
                        tipo='entrada',
                        user=request.user,
                        nf_recebida=nf,
                    )
                else:
                    messages.error(request, 'Erro ao lançar estoque.')
                    return render(request, 'fiscal/lancamento_nf.html', {'nf': nf, 'itens': itens})
            Titulo.objects.create(
                valor=nf.valor_total,
                data_vencimento=nf.data_emissao + timezone.timedelta(days=30),
                user=request.user,
                nf_recebida=nf,
                status='pendente',
            )
            nf.status = 'processada'
            nf.data_processamento = timezone.now()
            nf.save()
            messages.success(request, 'NF-e processada com sucesso. Estoque e financeiro atualizados.')
            return redirect('fiscal_historico')
        return render(request, 'fiscal/lancamento_nf.html', {'nf': nf, 'itens': itens})
    except NfRecebida.DoesNotExist:
        messages.error(request, 'NF-e não encontrada ou status inválido.')
        return redirect('fiscal_dashboard')

@login_required
def atualizar_notas(request):
    # Mock response while SEFAZ is disabled
    messages.info(request, 'Tarefa de atualização de NF-e não executada (SEFAZ desativada).')
    return redirect('fiscal_dashboard')

class HistoricoListView(ListView):
    model = NfRecebida
    template_name = 'fiscal/historico_lancamentos.html'
    context_object_name = 'nf_list'
    paginate_by = 20

    def get_queryset(self):
        return NfRecebida.objects.filter(user=self.request.user).order_by('-data_lancamento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_data'] = self.request.GET.get('data', '')
        return context