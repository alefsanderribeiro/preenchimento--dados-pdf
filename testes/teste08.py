from endesive import pdf
from datetime import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

def assinar_pdf(pdf_path, pfx_path, pfx_password, output_path):
    # Carregar o certificado PFX
    with open(pfx_path, 'rb') as pfx_file:
        pfx_data = pfx_file.read()
    
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pfx_data, pfx_password.encode(), backends.default_backend()
    )

    # Configurar dados da assinatura
    date = datetime.now().strftime("D:%Y%m%d%H%M%S-03'00'")
    dados_assinatura = {
        'sigflags': 3,
        'sigpage': 2,
        'sigbutton': True,
        'sigfield': 'Assinatura Digital',
        'auto_sigfield': False,
        'sigandcertify': True,
        'contact': 'Alefsander Ribeiro Nascimento',
        'location': 'São Paulo',
        'signingdate': date,
        'reason': 'Eu sou o autor deste documento',
        'signature': 'Alefsander Ribeiro Nascimento',
        'signaturebox': (0, 618627, 623359, 5983),
        'sigflagsft': 132,
        'signform': False,
        'signaturetype': 'adobe.ppklite',
    }

    # Assinar o PDF
    with open(pdf_path, 'rb') as pdf_file:
        datau = pdf_file.read()
    
    datas = pdf.cms.sign(datau, dados_assinatura,
                         private_key, certificate,
                         additional_certificates,
                         'sha256',
                         None)
    
    # Salvar o PDF assinado
    with open(output_path, 'wb') as output_file:
        output_file.write(datau)
        output_file.write(datas)

    print(f"PDF assinado salvo em: {output_path}")

# Exemplo de uso
pdf_path = 'filled-and-signed.pdf'
pfx_path = 'cert_digital_alefe_nova.pfx'
pfx_password = 'Senha123'
output_path = 'documento_assinado.pdf'

assinar_pdf(pdf_path, pfx_path, pfx_password, output_path)
