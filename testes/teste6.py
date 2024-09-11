from pypdf import PdfReader, PdfWriter
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding
from cryptography.hazmat.backends import default_backend
import io

def sign_pdf(input_pdf, output_pdf, pfx_file, pfx_password):
    # Carregar o certificado e a chave privada do arquivo .pfx
    with open(pfx_file, 'rb') as f:
        pfx_data = f.read()

    private_key, certificate, _ = pkcs12.load_key_and_certificates(
        pfx_data, pfx_password.encode(), default_backend()
    )

    # Ler o PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Copiar todas as páginas do PDF original
    for page in reader.pages:
        writer.add_page(page)

    # Criar a assinatura
    hash_value = hashes.Hash(hashes.SHA256())
    buff = io.BytesIO()
    writer.write(buff)
    hash_value.update(buff.getvalue())
    signature = private_key.sign(
        hash_value.finalize(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    

    # Adicionar a assinatura ao PDF
    writer.add_metadata({
        '/Signature': signature,
        '/SignatureCertificate': certificate.public_bytes(Encoding.DER)
    })

    # Salvar o PDF assinado
    with open(output_pdf, 'wb') as f:
        writer.write(f)

# Uso da função
input_pdf = 'filled-out-Final.pdf'
output_pdf = 'documento_assinado.pdf'
pfx_file = 'alefsander_cert.pfx'
pfx_password = 'Senha123'

sign_pdf(input_pdf, output_pdf, pfx_file, pfx_password)
print("PDF assinado com sucesso!")