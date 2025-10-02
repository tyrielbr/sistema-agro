from decouple import config
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

def load_certificate():
    """Carrega Cert A1 do .pfx."""
    path = config('CERT_A1_PATH')
    senha = config('CERT_A1_PASSWORD')
    if not os.path.exists(path):
        raise ValueError("Certificado A1 não encontrado no path especificado.")
    with open(path, 'rb') as f:
        pfx_data = f.read()
    p12 = serialization.pkcs12.load_key_and_certificates(pfx_data, senha.encode())
    return p12[0], p12[1]  # Chave privada, Certificado