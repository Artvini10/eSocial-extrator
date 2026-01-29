import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class WSConfig:
    envio_url: str
    consulta_url: str
    cert_path: str
    cert_password: str
    ca_bundle_path: str | None
    simulacao: bool

def carregar_ws_config(ambiente: str) -> WSConfig:
    cert_path = os.getenv("CERT_PATH")
    cert_password = os.getenv("CERT_PASSWORD")
    ca_bundle_path = os.getenv("CA_BUNDLE_PATH") or None
    simulacao = (os.getenv("SIMULACAO", "false").strip().lower() in ("1", "true", "yes", "y"))

    if not cert_path or not cert_password:
        raise RuntimeError("CERT_PATH/CERT_PASSWORD não configurados no .env")

    if ambiente == "producao":
        envio_url = os.getenv("ESOCIAL_ENVIO_URL_PRODUCAO")
        consulta_url = os.getenv("ESOCIAL_CONSULTA_URL_PRODUCAO")
    elif ambiente == "producao_restrita":
        envio_url = os.getenv("ESOCIAL_ENVIO_URL_PRODUCAO_RESTRITA")
        consulta_url = os.getenv("ESOCIAL_CONSULTA_URL_PRODUCAO_RESTRITA")
    else:
        raise ValueError("Ambiente inválido. Use: producao | producao_restrita")

    if not envio_url or not consulta_url:
        raise RuntimeError("URLs do WS não configuradas no .env (ESOCIAL_ENVIO_URL_* e ESOCIAL_CONSULTA_URL_*)")

    return WSConfig(
        envio_url=envio_url,
        consulta_url=consulta_url,
        cert_path=cert_path,
        cert_password=cert_password,
        ca_bundle_path=ca_bundle_path,
        simulacao=simulacao,
    )