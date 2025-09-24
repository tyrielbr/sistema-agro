from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Silo(models.Model):
    nome = models.CharField(max_length=100)
    capacidade = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

class Insumo(models.Model):
    CATEGORIA_CHOICES = [
        ('granel', 'Insumos Granel (Gesso, Calcário, etc.)'),
        ('lavoura', 'Insumos Lavoura (Semente, Herbicida, etc.)'),
        ('maquinas', 'Insumos Máquinas (Peças, Filtros, etc.)'),
    ]
    nome = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    unidade = models.CharField(max_length=20)
    silo = models.ForeignKey(Silo, on_delete=models.PROTECT)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        total_silo = Insumo.objects.filter(silo=self.silo).exclude(id=self.id).aggregate(models.Sum('quantidade'))['quantidade__sum'] or 0
        if total_silo + self.quantidade > self.silo.capacidade:
            raise ValidationError('Capacidade do silo excedida.')

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    silo = models.ForeignKey(Silo, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome