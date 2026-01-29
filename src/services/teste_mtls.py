import os
import sys
from dotenv import load_dotenv
from .mtls_client import criar_sessao_mtls_de_pfx

print(f"🐍 Python em uso: {sys.version.split()[0]}")

load_dotenv()

CERT_PATH = os.getenv("CERT_PATH")
CERT_PASSWORD = os.getenv("CERT_PASSWORD")
CA_BUNDLE_PATH = os.getenv("CA_BUNDLE_PATH") or None

if not CERT_PATH or not CERT_PASSWORD:
    raise RuntimeError("CERT_PATH ou CERT_PASSWORD não configurados no .env")

ctx = criar_sessao_mtls_de_pfx(CERT_PATH, CERT_PASSWORD, ca_bundle_path=CA_BUNDLE_PATH)

try:
    print("✅ Sessão mTLS criada. Cert e chave extraídos em arquivos temporários.")
    print("📡 Fazendo request HTTPS de teste...")

    # Endpoint de teste: não exige certificado do cliente, mas valida que seu HTTPS está ok.
    # Depois você troca pela URL real do WS do eSocial.
    resp = ctx.session.get("https://www.google.com", timeout=30)

    print(f"✅ HTTPS OK | status={resp.status_code}")
finally:
    ctx.close()
    print("🧹 Temporários removidos.")