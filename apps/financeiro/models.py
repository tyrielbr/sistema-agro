from django.db import models
from django_ledger.models.accounts import AccountModel
from django.contrib.auth.models import User
from apps.fiscal.models import NfRecebida

class ContaAgro(models.Model):
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    descricao = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.descricao

class Vencimento(models.Model):
    conta = models.ForeignKey(ContaAgro, on_delete=models.CASCADE)
    data_vencimento = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    quitado = models.BooleanField(default=False)
    anexo = models.FileField(upload_to='anexos/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Vencimento {self.conta} - {self.data_vencimento}"

class Contrato(models.Model):
    TIPO_CHOICES = [
        ('credito_obtido', 'Obtenção de Crédito'),
        ('credito_concedido', 'Concessão de Crédito'),
        ('venda_futura', 'Contrato de Venda Futura'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Contrato {self.tipo} - {self.data}"

class Financiamento(models.Model):
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    vencimentos = models.ManyToManyField(Vencimento)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.descricao

class Titulo(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nf_recebida = models.ForeignKey(NfRecebida, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='pendente')

    def __str__(self):
        return f"Título R$ {self.valor} - {self.status}"