import os
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv

print("🔐 Testando leitura de certificado A1 (.pfx)")

load_dotenv()

CERT_PATH = os.getenv("CERT_PATH")
CERT_PASSWORD = os.getenv("CERT_PASSWORD")

if not CERT_PATH or not CERT_PASSWORD:
    raise RuntimeError("CERT_PATH ou CERT_PASSWORD não configurados no .env")

print(f"📄 Arquivo: {CERT_PATH}")

with open(CERT_PATH, "rb") as f:
    pfx_data = f.read()

private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
    pfx_data,
    CERT_PASSWORD.encode(),
    backend=default_backend()
)

if private_key and certificate:
    print("✅ Certificado carregado com sucesso!")
    print("🔑 Chave privada OK")
    print("📜 Certificado público OK")
else:
    raise RuntimeError("❌ Falha ao extrair chave ou certificado")