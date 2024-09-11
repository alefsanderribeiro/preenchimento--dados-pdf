from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec
from pyhanko_certvalidator import ValidationContext
from pyhanko.sign.validation import validate_pdf_signature
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding
from cryptography.hazmat.backends import default_backend



# Carregar o certificado e a chave privada do arquivo .pfx
# Carregar o certificado e a chave privada do arquivo .pfx


input_pdf = 'filled-out-Final.pdf'
output_pdf = 'documento_assinado.pdf'
pfx_file = 'alefsander_cert.pfx'
pfx_password = 'Senha123'
with open(pfx_file, 'rb') as f:
    pfx_data = f.read()

private_key, certificate, _ = pkcs12.load_key_and_certificates(
    pfx_data, pfx_password.encode(), default_backend()
)

signer = signers.SimpleSigner.load(private_key, cert_file=pfx_file, key_passphrase=pfx_password)

print(signer)


# Abrir o PDF
with open('filled-out-Final - Copia.pdf', 'rb') as doc:
    w = IncrementalPdfFileWriter(doc)
    
    # Adicionar um campo de assinatura
    sig_field = SigFieldSpec('Assinatura Digital')
    
    # Assinar o documento
    out = signers.sign_pdf(
        w,
        signers.PdfSignatureMetadata(field_name='Assinatura Digital'),
        signer=signer,
        output='documento_assinado.pdf',
        new_field_spec=sig_field
    )

# Validar a assinatura (opcional)
with open('documento_assinado.pdf', 'rb') as doc:
    validation_context = ValidationContext(allow_fetching=True)
    sig = validate_pdf_signature(doc, signer_validation_context=validation_context)
    print(sig.summary())
    
    
    