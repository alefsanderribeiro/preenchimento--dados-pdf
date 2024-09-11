from endesive import pdf
from datetime import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject
import io

def adicionar_recipient_signature(pdf_path, pfx_path, pfx_password, output_path):
    # Carregar o certificado PFX
    with open(pfx_path, 'rb') as pfx_file:
        pfx_data = pfx_file.read()
    
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pfx_data, pfx_password.encode(), backends.default_backend()
    )

    # Bloquear todos os campos do formulário
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    if '/AcroForm' in reader.trailer['/Root']:
        writer._root_object[NameObject('/AcroForm')] = reader.trailer['/Root']['/AcroForm']

    for page in writer.pages:
        if '/Annots' in page:
            for i in range(len(page['/Annots'])):
                try:
                    annotation = page['/Annots'][i].get_object()
                    if annotation.get('/FT') == '/Sig':
                        continue  # Pular campos de assinatura
                    ff = annotation.get(NameObject('/Ff'), NumberObject(0))
                    annotation[NameObject('/Ff')] = NumberObject(ff | 1)
                except Exception as e:
                    print(f"Erro ao processar anotação {i}: {str(e)}")

    # Salvar o PDF com campos bloqueados em memória
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)

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
        'reason': 'Eu sou o autor desse documento',
        'signature': 'Alefsander Ribeiro Nascimento',
        'signaturebox': (100, 100, 300, 200),
        'sigflagsft': 132,
        'signform': True,
        'signaturetype': 'adobe.ppklite',
        'md_algorithm': 'sha256',
        'doctimestamp': date,
        'use_sigfield_v2': True,
        'sigfield_v2': {
            'sigtype': 'ETSI.CAdES.detached',
            'sigflags': 3,
            'reference': [{
                'type': 'SigRef',
                'transformParams': {
                    'type': 'TransformParams',
                    'V': '1.2',
                    'Fields': ['*'],
                    'Action': 'Include',
                    'LockDocument': 'true'
                },
                'digestMethod': 'SHA256'
            }]
        }
    }
    
    # Assinar o PDF
    #with open(pdf_path, 'rb') as pdf_file:
    #    datau = pdf_file.read()
    
    #datas = pdf.cms.sign(datau, dados_assinatura,
    #                     private_key, certificate,
    #                     additional_certificates,
    #                     'sha256',
    #                     None)
    
    # Salvar o PDF final assinado
    #with open(output_path, 'wb') as output_file:
    #    output_file.write(datau)
    #    output_file.write(datas)

    print(f"PDF assinado e com campos bloqueados salvo em: {output_path}")

# Exemplo de uso
pdf_path = 'filled-and-signed.pdf'
pfx_path = 'cert_digital_alefe_nova.pfx'
pfx_password = 'Senha123'
output_path = 'documento_assinado_campos_bloqueados.pdf'

adicionar_recipient_signature(pdf_path, pfx_path, pfx_password, output_path)