from endesive import pdf
from datetime import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12


def adicionar_recipient_signature(pdf_path, pfx_path, pfx_password, output_path):
    # Carregar o certificado PFX
    with open(pfx_path, 'rb') as pfx_file:
        pfx_data = pfx_file.read()
    
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pfx_data, pfx_password.encode(), backends.default_backend()
    )

    # Configurar dados da assinatura
    date = datetime.now().strftime("D:%Y%m%d%H%M%S-04'00'")
    dados_assinatura = {
        'sigflags': 3,  # Alterado para 0 para indicar uma assinatura de destinatário
        'sigpage': 2,
        'sigbutton': True,
        'sigfield': 'Assinatura Digital',  # Nome do campo para a assinatura de destinatário
        'auto_sigfield': False,  # Alterado para True para criar um novo campo de assinatura
        'sigandcertify': True,  # Alterado para False para não certificar o documento
        'contact': 'Alefsander Ribeiro Nascimento', #Nome do assinante. Mesmo do Certificado
        'location': 'São Paulo', # Local da assinatura
        'signingdate': date,
        'reason': 'Eu sou o autor desse documento', #Razão da assinatura. 
        'signature': 'Alefsander Ribeiro Nascimento',
        'signaturebox': (100, 100, 300, 200),  # Ajuste as coordenadas conforme necessário
        'sigflagsft': 132,  # Alterado para 0 para uma assinatura de destinatário
        'signform': True, # Mantém signform como False, o que significa que não está assinando o formulário inteiro.

        'signaturetype': 'adobe.ppklite',
        # Adicionar propriedade para tornar o documento somente leitura
        'lock': True,
        # Configurar as permissões de modificação
        'docmdp': 1  # 1 = Nenhuma alteração permitida
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

    print(f"PDF com assinatura de destinatário salvo em: {output_path}")

# Exemplo de uso
pdf_path = 'filled-and-signed.pdf'  # Use o PDF já assinado como entrada
pfx_path = 'cert_digital_alefe_nova.pfx'
pfx_password = 'Senha123'
output_path = 'documento_com_recipient_signature.pdf'

adicionar_recipient_signature(pdf_path, pfx_path, pfx_password, output_path)
