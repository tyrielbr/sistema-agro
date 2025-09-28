
from celery import shared_task
from .utils import load_certificate

from django.contrib.auth.models import User
from .models import NfRecebida, ItemNf
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

@shared_task
def download_nf_diaria(user_id):
    try:
        logger.info(f"Iniciando tarefa download_nf_diaria para user_id={user_id}")
        user = User.objects.get(id=user_id)
        if not hasattr(user, 'profile') or not user.profile.cnpj:
            logger.error("UserProfile ou CNPJ não encontrado para o usuário.")
            raise ValueError("UserProfile ou CNPJ não encontrado.")
        key, cert = load_certificate()
        logger.info("Certificado carregado com sucesso.")
        distribuicao = NFeDistribuicaoDFe(
            cnpj=user.profile.cnpj,
            cert=cert,
            key=key,
            ambiente='homologacao',  # Change to 'producao' in production
            uf='SP',  # Adjust to your UF
        )
        logger.info(f"Consultando SEFAZ com CNPJ={user.profile.cnpj}, UF=SP, ambiente=homologacao")
        result = distribuicao.consultar(ultNSU=0)
        logger.info(f"Resposta da SEFAZ: {result}")
        nfe_count = 0
        for nfe in result.get('nfeProc', []):
            xml_content = ET.tostring(nfe, encoding='unicode')
            nf = NfRecebida.objects.create(
                chave_nfe=nfe['chave'],
                xml_content=xml_content,
                data_emissao=nfe['dhEmi'],
                valor_total=nfe['vNF'],
                emitente_cnpj=nfe['emit']['CNPJ'],
                user=user,
            )
            logger.info(f"NF-e criada: {nf.chave_nfe}")
            for item in nfe['det']:
                ItemNf.objects.create(
                    nf_recebida=nf,
                    produto=item['prod']['xProd'],
                    ncm=item['prod']['NCM'],
                    quantidade=item['prod']['qCom'],
                    valor_unitario=item['prod']['vUnCom'],
                )
            nfe_count += 1
        logger.info(f"Total de NF-e processadas: {nfe_count}")
        return nfe_count
    except Exception as e:
        logger.error(f"Erro na tarefa download_nf_diaria: {str(e)}")
        raise
