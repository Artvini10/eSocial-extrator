import os
import ssl
import tempfile
from dataclasses import dataclass
from typing import Optional

import requests
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption, pkcs12


@dataclass
class MTLSContext:
    session: requests.Session
    cert_path: str
    key_path: str
    ca_bundle_path: Optional[str]

    def close(self) -> None:
        try:
            self.session.close()
        finally:
            for p in (self.cert_path, self.key_path):
                try:
                    os.remove(p)
                except Exception:
                    pass


def criar_sessao_mtls_de_pfx(pfx_path: str, password: str, ca_bundle_path: Optional[str] = None) -> MTLSContext:
    with open(pfx_path, "rb") as f:
        pfx_data = f.read()

    private_key, certificate, _additional = pkcs12.load_key_and_certificates(
        pfx_data, password.encode("utf-8")
    )

    if private_key is None or certificate is None:
        raise RuntimeError("Não foi possível extrair chave privada e certificado do .pfx (senha/certificado inválidos).")

    cert_pem = certificate.public_bytes(Encoding.PEM)
    key_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption(),
    )

    cert_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
    key_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")

    cert_tmp.write(cert_pem)
    cert_tmp.flush()
    cert_tmp.close()

    key_tmp.write(key_pem)
    key_tmp.flush()
    key_tmp.close()

    sess = requests.Session()
    sess.cert = (cert_tmp.name, key_tmp.name)

    if ca_bundle_path:
        sess.verify = ca_bundle_path
    else:
        sess.verify = True

    return MTLSContext(session=sess, cert_path=cert_tmp.name, key_path=key_tmp.name, ca_bundle_path=ca_bundle_path)