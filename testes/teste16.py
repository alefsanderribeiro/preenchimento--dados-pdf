from endesive import pdf
from datetime import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject

def assinar_digital(pdf_path, pfx_path, pfx_password, output_path):
    
    
            
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
    
    
    print("PDF Assinado!!!!!")
    
    
"""
def bloquear_campos(pdf_path, output_path):
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

    # Salvar o PDF final com campos bloqueados
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    print(f"PDF assinado e com campos bloqueados salvo em: {output_path}")
    
    """
def bloquear_campos(pdf_path, output_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Copiar todas as páginas do PDF original
    for page in reader.pages:
        writer.add_page(page)

    # Copiar os metadados e outras informações do PDF original
    writer._info = reader.metadata
    writer._ID = reader.xmp_metadata

    if '/AcroForm' in reader.trailer['/Root']:
        writer._root_object[NameObject('/AcroForm')] = reader.trailer['/Root']['/AcroForm']

    # Bloquear os campos do formulário
    for page in writer.pages:
        if '/Annots' in page:
            for i, annotation in enumerate(page['/Annots']):
                try:
                    annotation_object = annotation.get_object()
                    if annotation_object.get('/FT') == '/Sig':
                        continue  # Pular campos de assinatura
                    ff = annotation_object.get(NameObject('/Ff'), NumberObject(0))
                    annotation_object[NameObject('/Ff')] = NumberObject(ff | 1)
                except Exception as e:
                    print(f"Erro ao processar anotação {i}: {str(e)}")

    # Salvar o PDF final com campos bloqueados
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    print(f"PDF com campos bloqueados salvo em: {output_path}")



# Exemplo de uso
pdf_path = 'filled-and-signed.pdf'
pfx_path = 'cert_digital_alefe_nova.pfx'
pfx_password = 'Senha123'
output_path = 'documento_assinado_campos_bloqueados.pdf'


#bloquear_campos(pdf_path, output_path)

assinar_digital(pdf_path, pfx_path, pfx_password, output_path)
