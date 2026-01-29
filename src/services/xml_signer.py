from lxml import etree
from signxml import XMLSigner
from cryptography.hazmat.primitives.serialization import Encoding

def assinar_xml(xml_str: str, private_key, certificate):
    signer = XMLSigner(
        method="enveloped",
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256"
    )

    xml = etree.fromstring(xml_str.encode())
    signed_xml = signer.sign(
        xml,
        key=private_key,
        cert=certificate.public_bytes(Encoding.PEM)
    )

    return etree.tostring(signed_xml)