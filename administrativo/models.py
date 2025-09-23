from django.db import models
from agricola.models import OrdemServico
from django.contrib.auth.models import User

class CentroCusto(models.Model):
    nome = models.CharField(max_length=100)
    ordens_associadas = models.ManyToManyField(OrdemServico)
    custo_rateado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def calcular_rateio(self):
        total_area = sum(ordem.talhao.area for ordem in self.ordens_associadas.all() if ordem.talhao)
        if total_area > 0:
            for ordem in self.ordens_associadas.all():
                ordem.custo_total = (ordem.talhao.area / total_area) * self.custo_rateado
                ordem.save()

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    CONDICAO_CHOICES = [
        ('diarista', 'Diarista'),
        ('temporario', 'Temporário'),
        ('registrado', 'Registrado'),
    ]
    nome = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=20, blank=True)
    telefone = models.CharField(max_length=15, blank=True)
    endereco = models.TextField(blank=True)
    condicao = models.CharField(max_length=20, choices=CONDICAO_CHOICES)
    salario_registrado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salario_efetivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_hora_extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Sugestão: 50%
    valor_diaria_extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Sugestão: 100%
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        hora_normal = self.salario_efetivo / 220  # Assumindo 220h/mês
        if not self.valor_hora_extra:
            self.valor_hora_extra = hora_normal * 1.5  # 50% extra
        if not self.valor_diaria_extra:
            self.valor_diaria_extra = self.salario_efetivo * 2  # 100% para domingos/feriados
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome