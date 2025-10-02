from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_cpf_cnpj(value):
    """Valida se o valor é um CPF (11 dígitos) ou CNPJ (14 dígitos)."""
    value = ''.join(filter(str.isdigit, str(value)))  # Remove caracteres não numéricos
    if len(value) not in (11, 14):
        raise ValidationError('CPF deve ter 11 dígitos e CNPJ deve ter 14 dígitos.')
    return value

class Pessoa(models.Model):
    TIPO_CHOICES = [
        ('proprietario', 'Proprietário'),
        ('socio', 'Sócio'),
    ]
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=14, validators=[validate_cpf_cnpj])
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='proprietario')
    poder_decisao = models.BooleanField(default=False)  # True para proprietário com poder de decisão final
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

class Fazenda(models.Model):
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=200)
    area_total = models.DecimalField(max_digits=10, decimal_places=2)
    proprietarios_socios = models.ManyToManyField(Pessoa)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.proprietarios_socios.count() == 0:
            raise ValidationError('Cadastre pelo menos um proprietário ou sócio antes de cadastrar a fazenda.')

        # Validação de hierarquia será feita em Area/Talhao

    def __str__(self):
        return self.nome

class Arrendamento(models.Model):
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=200)
    area_total = models.DecimalField(max_digits=10, decimal_places=2)
    proprietarios_socios = models.ManyToManyField(Pessoa)
    contrato = models.FileField(upload_to='contratos/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if not self.contrato:
            raise ValidationError('Um contrato é obrigatório para arrendamentos.')

    def __str__(self):
        return self.nome

class Area(models.Model):
    nome = models.CharField(max_length=100)
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, null=True, blank=True)
    arrendamento = models.ForeignKey(Arrendamento, on_delete=models.CASCADE, null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    kmz_file = models.FileField(upload_to='kmz/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.fazenda and self.arrendamento:
            raise ValidationError('Uma área não pode pertencer a uma fazenda e um arrendamento ao mesmo tempo.')
        if not self.fazenda and not self.arrendamento:
            raise ValidationError('Uma área deve pertencer a uma fazenda ou arrendamento.')
        
        # Validação de soma de talhões apenas se o objeto já tiver PK (i.e., já salvo)
        if self.pk:
            total_talhoes = self.talhao_set.aggregate(total=models.Sum('area_size'))['total'] or 0
            if total_talhoes > self.area:
                raise ValidationError('A soma dos talhões excede a área total.')
            # Validação com superior (fazenda/arrendamento)
            if self.fazenda:
                total_areas = self.fazenda.area_set.aggregate(total=models.Sum('area'))['total'] or 0
                if total_areas > self.fazenda.area_total:
                    raise ValidationError('A soma das áreas excede a área total da fazenda.')
            elif self.arrendamento:
                total_areas = self.arrendamento.area_set.aggregate(total=models.Sum('area'))['total'] or 0
                if total_areas > self.arrendamento.area_total:
                    raise ValidationError('A soma das áreas excede a área total do arrendamento.')

    def __str__(self):
        return self.nome

class Talhao(models.Model):
    nome = models.CharField(max_length=100)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    area_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Nullable para migração
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    kmz_file = models.FileField(upload_to='kmz/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.area_size is not None and self.area_size > self.area.area:
            raise ValidationError('O talhão não pode ser maior que a área.')

    def __str__(self):
        return self.nome