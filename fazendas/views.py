from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.conf import settings
from .models import Pessoa, Fazenda, Arrendamento, Area, Talhao
from .forms import PessoaForm, FazendaForm, ArrendamentoForm, AreaForm, TalhaoForm
from django.db import models

@login_required
def dashboard(request):
    context = {}
    return render(request, 'fazendas/dashboard.html', context)

@login_required
def cria_pessoa(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST)
        if form.is_valid():
            pessoa = form.save(commit=False)
            pessoa.owner = request.user
            pessoa.save()
            messages.success(request, 'Proprietário/Sócio cadastrado com sucesso.')
            return redirect('fazendas_dashboard')
    else:
        form = PessoaForm()
    return render(request, 'fazendas/cria_pessoa.html', {'form': form})

class PessoaUpdateView(UpdateView):
    model = Pessoa
    form_class = PessoaForm
    template_name = 'fazendas/edita_pessoa.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Proprietário/Sócio editado com sucesso.')
        return super().form_valid(form)

class PessoaDeleteView(DeleteView):
    model = Pessoa
    template_name = 'fazendas/confirma_delete.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Proprietário/Sócio removido com sucesso.')
        return super().delete(request, *args, **kwargs)

@login_required
def cria_fazenda(request):
    if Pessoa.objects.filter(owner=request.user).count() == 0:
        messages.error(request, 'Cadastre pelo menos um proprietário ou sócio antes de cadastrar uma fazenda.')
        return redirect('cria_pessoa')
    if request.method == 'POST':
        form = FazendaForm(request.POST)
        if form.is_valid():
            fazenda = form.save(commit=False)
            fazenda.owner = request.user
            fazenda.save()
            form.save_m2m()
            messages.success(request, 'Fazenda cadastrada com sucesso.')
            return redirect('fazendas_dashboard')
    else:
        form = FazendaForm()
    return render(request, 'fazendas/cria_fazenda.html', {'form': form})

class FazendaUpdateView(UpdateView):
    model = Fazenda
    form_class = FazendaForm
    template_name = 'fazendas/edita_fazenda.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Fazenda editada com sucesso.')
        return super().form_valid(form)

class FazendaDeleteView(DeleteView):
    model = Fazenda
    template_name = 'fazendas/confirma_delete.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Fazenda removida com sucesso.')
        return super().delete(request, *args, **kwargs)

@login_required
def cria_arrendamento(request):
    if Pessoa.objects.filter(owner=request.user).count() == 0:
        messages.error(request, 'Cadastre pelo menos um proprietário ou sócio antes de cadastrar um arrendamento.')
        return redirect('cria_pessoa')
    if request.method == 'POST':
        form = ArrendamentoForm(request.POST, request.FILES)
        if form.is_valid():
            arrendamento = form.save(commit=False)
            arrendamento.owner = request.user
            arrendamento.save()
            form.save_m2m()  # Salva a relação ManyToMany após o objeto ser salvo
            messages.success(request, 'Arrendamento cadastrado com sucesso.')
            return redirect('fazendas_dashboard')
        else:
            messages.error(request, 'Erro ao cadastrar arrendamento. Verifique os dados.')
    else:
        form = ArrendamentoForm()
    return render(request, 'fazendas/cria_arrendamento.html', {'form': form})
      
class ArrendamentoUpdateView(UpdateView):
    model = Arrendamento
    form_class = ArrendamentoForm
    template_name = 'fazendas/edita_arrendamento.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Arrendamento editado com sucesso.')
        return super().form_valid(form)

class ArrendamentoDeleteView(DeleteView):
    model = Arrendamento
    template_name = 'fazendas/confirma_delete.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Arrendamento removido com sucesso.')
        return super().delete(request, *args, **kwargs)

@login_required
def cria_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST, request.FILES)
        if form.is_valid():
            area = form.save(commit=False)
            area.owner = request.user
            area.save()
            messages.success(request, 'Área cadastrada com sucesso.')
            return redirect('fazendas_dashboard')
    else:
        form = AreaForm()
    return render(request, 'fazendas/cria_area.html', {'form': form})

class AreaUpdateView(UpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'fazendas/edita_area.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Área editada com sucesso.')
        return super().form_valid(form)

class AreaDeleteView(DeleteView):
    model = Area
    template_name = 'fazendas/confirma_delete.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Área removida com sucesso.')
        return super().delete(request, *args, **kwargs)

@login_required
def cria_talhao(request):
    if request.method == 'POST':
        form = TalhaoForm(request.POST, request.FILES)
        if form.is_valid():
            talhao = form.save(commit=False)
            talhao.owner = request.user
            talhao.save()
            messages.success(request, 'Talhão cadastrado com sucesso.')
            return redirect('fazendas_dashboard')
    else:
        form = TalhaoForm()
    return render(request, 'fazendas/cria_talhao.html', {'form': form})

class TalhaoUpdateView(UpdateView):
    model = Talhao
    form_class = TalhaoForm
    template_name = 'fazendas/edita_talhao.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Talhão editado com sucesso.')
        return super().form_valid(form)

class TalhaoDeleteView(DeleteView):
    model = Talhao
    template_name = 'fazendas/confirma_delete.html'
    success_url = reverse_lazy('fazendas_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Talhão removido com sucesso.')
        return super().delete(request, *args, **kwargs)

@login_required
def lista_propriedades(request):
    fazendas = Fazenda.objects.filter(owner=request.user)
    arrendamentos = Arrendamento.objects.filter(owner=request.user)
    context = {'fazendas': fazendas, 'arrendamentos': arrendamentos}
    return render(request, 'fazendas/lista_propriedades.html', context)

@login_required
def detalhes_propriedade(request, tipo, id):
    if tipo == 'fazenda':
        propriedade = get_object_or_404(Fazenda, id=id, owner=request.user)
    elif tipo == 'arrendamento':
        propriedade = get_object_or_404(Arrendamento, id=id, owner=request.user)
    else:
        return redirect('fazendas_dashboard')
    areas = propriedade.area_set.all()
    context = {'propriedade': propriedade, 'areas': areas}
    return render(request, 'fazendas/detalhes_propriedade.html', context)

@login_required
def detalhes_area(request, id):
    area = get_object_or_404(Area, id=id, owner=request.user)
    talhoes = area.talhao_set.all()
    context = {'area': area, 'talhoes': talhoes, 'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY}
    return render(request, 'fazendas/detalhes_area.html', context)