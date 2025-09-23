from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User  # Para owner (multi-tenancy)

def validate_cpf_cnpj(value):
    if len(value) not in [11, 14]:
        raise ValidationError('CPF (11 dígitos) ou CNPJ (14 dígitos) inválido.')

class Proprietario(models.Model):
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=14, validators=[validate_cpf_cnpj])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Para multi-tenancy

    def __str__(self):
        return self.nome

class Fazenda(models.Model):
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=200)
    area_total = models.DecimalField(max_digits=10, decimal_places=2)
    proprietario = models.ForeignKey(Proprietario, null=True, blank=True, on_delete=models.SET_NULL)
    contrato_arrendamento = models.FileField(upload_to='contratos/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nome

class Talhao(models.Model):
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    coordenadas = models.JSONField()
    cultura_atual = models.ForeignKey('agricola.Cultura', null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def clean(self):
        total_area_talhoes = Talhao.objects.filter(fazenda=self.fazenda).exclude(id=self.id).aggregate(models.Sum('area'))['area__sum'] or 0
        if total_area_talhoes + self.area > self.fazenda.area_total * 1.05:
            raise ValidationError('Sobreposição de área excede 5% da fazenda.')

    def __str__(self):
        return f"{self.nome} ({self.fazenda})"