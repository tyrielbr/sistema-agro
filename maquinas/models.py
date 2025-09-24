from django.db import models
from django.contrib.auth.models import User

class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    ano = models.IntegerField()
    horas_registradas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    km_registrados = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nota_fiscal = models.FileField(upload_to='notas/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.marca}, {self.ano})"

class Maquina(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateField()
    vida_util_anos = models.IntegerField()
    depreciacao_anual = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.depreciacao_anual = self.valor_compra / self.vida_util_anos
        super().save(*args, **kwargs)

    def __str__(self):
        return self.equipamento.nome

class Manutencao(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    data = models.DateField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Manutenção {self.maquina} - {self.data}"

class Abastecimento(models.Model):
    PRODUTO_CHOICES = [
        ('oleo_diesel', 'Óleo Diesel'),
        ('arla', 'Arla'),
        ('oleo_lubrificante', 'Óleo Lubrificante'),
    ]
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    produto = models.CharField(max_length=20, choices=PRODUTO_CHOICES)
    quantidade_litros = models.DecimalField(max_digits=10, decimal_places=2)
    horimetro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_abastecimento = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Abastecimento {self.equipamento} - {self.data_abastecimento}"