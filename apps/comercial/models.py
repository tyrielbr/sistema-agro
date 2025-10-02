from django.db import models
from django.contrib.auth.models import User
from apps.fazendas.models import validate_cpf_cnpj

class FornecedorCliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=14, validators=[validate_cpf_cnpj])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

class CompraVenda(models.Model):
    TIPO_CHOICES = [
        ('compra', 'Compra'),
        ('venda', 'Venda'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fornecedor_cliente = models.ForeignKey(FornecedorCliente, on_delete=models.PROTECT)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    produtos = models.ManyToManyField('estoque.Produto')
    centro_custo = models.ForeignKey('administrativo.CentroCusto', null=True, blank=True, on_delete=models.SET_NULL)
    condicoes_pagamento = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo.capitalize()} {self.id} - {self.fornecedor_cliente}"