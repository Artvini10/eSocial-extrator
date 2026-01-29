from cryptography.hazmat.primitives.serialization import pkcs12

def carregar_certificado_pfx(pfx_bytes: bytes, senha: str):
    """
    Carrega certificado e chave privada de arquivo PFX.
    
    Args:
        pfx_bytes: Conteúdo binário do arquivo .pfx
        senha: Senha do certificado
    
    Returns:
        Tupla de (private_key, certificate, additional_certs)
    
    Raises:
        ValueError: Se a senha estiver incorreta ou formato inválido
    """
    try:
        private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
            pfx_bytes,
            senha.encode()
        )
        
        if private_key is None or certificate is None:
            raise ValueError("Certificado PFX não contém chave privada ou certificado válido")
        
        return private_key, certificate, additional_certs
    except Exception as e:
        raise ValueError(f"Erro ao carregar certificado PFX: {str(e)}")