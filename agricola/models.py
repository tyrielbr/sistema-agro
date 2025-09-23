from django.db import models
from django.core.exceptions import ValidationError
from fazendas.models import Talhao
from estoque.models import Insumo
from django.contrib.auth.models import User

class Cultura(models.Model):
    nome = models.CharField(max_length=50)
    periodo_ideal_inicio = models.DateField()
    periodo_ideal_fim = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nome

class OrdemServico(models.Model):
    talhao = models.ForeignKey(Talhao, on_delete=models.PROTECT)
    cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=50, choices=[('preparo', 'Preparo'), ('plantio', 'Plantio'), ('pulverizacao', 'Pulverização'), ('colheita', 'Colheita')])
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    insumos_usados = models.ManyToManyField(Insumo, through='UsoInsumo')
    aprovado = models.BooleanField(default=False)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    planejada = models.BooleanField(default=False)  # Para ordens planejadas vs. realizadas
    produtividade = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Para histórico (ex.: kg/ha)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def clean(self):
        if self.data_inicio < self.cultura.periodo_ideal_inicio or self.data_inicio > self.cultura.periodo_ideal_fim:
            raise ValidationError('Data fora do período ideal da cultura.')

    def __str__(self):
        return f"OS {self.id} - {self.tipo} ({self.talhao})"

class UsoInsumo(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=8, decimal_places=2)

    def clean(self):
        if self.quantidade > self.insumo.quantidade:
            raise ValidationError('Quantidade de insumo insuficiente.')

    def __str__(self):
        return f"{self.insumo} ({self.quantidade})"