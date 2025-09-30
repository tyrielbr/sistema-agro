from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date

class Cultura(models.Model):
    nome = models.CharField(max_length=50)
    periodo_ideal_inicio = models.DateField()
    periodo_ideal_fim = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ciclo_min = models.PositiveIntegerField(null=True, blank=True, help_text="Ciclo mínimo em dias (90-120)")
    ciclo_max = models.PositiveIntegerField(null=True, blank=True, help_text="Ciclo máximo em dias (90-120)")
    classificacao = models.CharField(max_length=50, choices=[
        ('grao', 'Grão'),
        ('leguminosa', 'Leguminosa'),
        ('hortalica', 'Hortaliça'),
        ('perene', 'Perene'),
        ('outra', 'Outra')
    ], null=True, blank=True)
    necessidade_hidrica = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Necessidade hídrica em mm ou m³/ha")
    observacoes = models.TextField(blank=True, help_text="Dicas de manejo ou informações adicionais")

    def __str__(self):
        return self.nome

    def clean(self):
        if self.ciclo_min and self.ciclo_max and (self.ciclo_min < 90 or self.ciclo_max > 120 or self.ciclo_min > self.ciclo_max):
            raise ValidationError('Ciclo deve estar entre 90 e 120 dias, com mínimo menor que máximo.')

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=[
        ('fixo', 'Fixo'),
        ('temporario', 'Temporário'),
        ('diarista', 'Diarista'),
    ])
    custo_diaria = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Custo por dia ou hora")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='agricola_funcionarios')

    def __str__(self):
        return f"{self.nome} ({self.tipo})"

class Lavoura(models.Model):
    talhao = models.ForeignKey('fazendas.Talhao', on_delete=models.PROTECT, related_name='lavouras')
    cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    data_plantio = models.DateField()
    irrigado = models.BooleanField(default=False, help_text="Marque se é irrigado (sequeiro se falso)")
    ativo = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Lavoura {self.id} - {self.cultura.nome} ({self.talhao.nome})"

    def clean(self):
        if not self.talhao:
            raise ValidationError('Talhão é obrigatório.')
        if self.data_plantio < self.cultura.periodo_ideal_inicio or self.data_plantio > self.cultura.periodo_ideal_fim:
            raise ValidationError('Data fora do período ideal da cultura.')

class OrdemServico(models.Model):
    titulo = models.CharField(max_length=100, blank=True)
    observacoes = models.TextField(blank=True)
    anexo = models.FileField(upload_to='anexos/', null=True, blank=True)
    talhao = models.ManyToManyField('fazendas.Talhao')  # Mudança pra múltiplos talhões
    cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=50, choices=[
        ('preparo', 'Preparo'),
        ('plantio', 'Plantio'),
        ('pulverizacao', 'Pulverização'),
        ('colheita', 'Colheita'),
        ('fertirrigacao', 'Fertirrigação'),
        ('irrigacao', 'Irrigação')
    ])
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    insumos_usados = models.ManyToManyField('estoque.Insumo', through='UsoInsumo', blank=True)
    aprovado = models.BooleanField(default=False)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    planejada = models.BooleanField(default=False)
    produtividade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume_agua = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Volume de água em m³ (para irrigação/fertirrigação)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.data_inicio < self.cultura.periodo_ideal_inicio or self.data_inicio > self.cultura.periodo_ideal_fim:
            raise ValidationError('Data fora do período ideal da cultura.')
        if self.tipo in ['fertirrigacao', 'irrigacao'] and not self.volume_agua:
            raise ValidationError('Volume de água é obrigatório para fertirrigação ou irrigação.')

    def __str__(self):
        return f"OS {self.id} - {self.tipo} ({self.talhao})"

class UsoInsumo(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    insumo = models.ForeignKey('estoque.Insumo', on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    receita_por_ha = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Receita por hectare (ex: 200 ml/ha)")
    unidade_medida = models.CharField(max_length=20, choices=[
        ('ml/ha', 'ml/ha'),
        ('kg/ha', 'kg/ha'),
        ('l/ha', 'l/ha'),
        ('g/ha', 'g/ha')
    ], null=True, blank=True)

    def clean(self):
        area_total = sum(talhao.area for talhao in self.ordem_servico.talhao.all()) if self.ordem_servico.talhao.all() else 0
        if self.receita_por_ha and area_total:
            self.quantidade = self.receita_por_ha * area_total
        if self.quantidade and self.quantidade > self.insumo.quantidade:
            raise ValidationError('Quantidade de insumo insuficiente.')
        if self.ordem_servico.tipo == 'fertirrigacao' and self.insumo.categoria != 'fertilizante':
            raise ValidationError('Insumo para fertirrigação deve ser fertilizante.')

    def save(self, *args, **kwargs):
        self.clean()
        if self.ordem_servico.aprovado and self.quantidade:
            self.insumo.quantidade -= self.quantidade
            self.insumo.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.insumo} ({self.quantidade})"