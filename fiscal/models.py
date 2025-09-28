
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import xml.etree.ElementTree as ET

class NfRecebida(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('ciencia', 'Ciência'),
        ('rejeitada', 'Rejeitada'),
        ('pendente processamento', 'Pendente Processamento'),
        ('processada', 'Processada'),
    ]
    chave_nfe = models.CharField(max_length=44, unique=True)
    xml_content = models.TextField()  # XML original
    data_emissao = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    emitente_cnpj = models.CharField(max_length=18)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pendente')
    motivo_rejeicao = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_lancamento = models.DateTimeField(auto_now_add=True)
    data_processamento = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if len(self.chave_nfe) != 44:
            raise ValidationError('Chave NF-e deve ter exatamente 44 caracteres.')

    def validate_xml(self):
        try:
            root = ET.fromstring(self.xml_content)
            return True
        except ET.ParseError:
            raise ValidationError('XML inválido.')
        return False

    def __str__(self):
        return f"NF-e {self.chave_nfe}"

class ItemNf(models.Model):
    nf_recebida = models.ForeignKey(NfRecebida, on_delete=models.CASCADE, related_name='itens')
    produto = models.CharField(max_length=100)
    ncm = models.CharField(max_length=20)
    quantidade = models.DecimalField(max_digits=10, decimal_places=3)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total_item = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_item = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto} - {self.quantidade} un"

class LancamentoEstoque(models.Model):
    nf_recebida = models.ForeignKey(NfRecebida, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(ItemNf, on_delete=models.CASCADE)
    quantidade_confirmada = models.DecimalField(max_digits=10, decimal_places=3)
    lote = models.CharField(max_length=50, blank=True)
    data_lancamento = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Lançamento {self.item} - {self.quantidade_confirmada} un"