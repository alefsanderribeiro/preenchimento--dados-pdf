import pypdf
from pypdf import 

# Caminhos dos arquivos
input_pdf_path = 'filled-out-Final.pdf'
output_pdf_path = 'arquivo_assinado.pdf'
cert_path = 'alefsander_cert.pfx'
cert_password = 'Senha123'

# Preencher os campos do PDF
def preencher_campos_pdf(input_pdf_path, output_pdf_path, dados):
    pdf_reader = pypdf.PdfReader(input_pdf_path)
    pdf_writer = pypdf.PdfWriter()

    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        pdf_writer.addPage(page)

    # Preencher os campos do formulário
    pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(0), dados)

    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

# Dados a serem preenchidos no PDF
dados = {
    'campo1': 'valor1',
    'campo2': 'valor2',
    # Adicione mais campos conforme necessário
}

# Preencher os campos do PDF
preencher_campos_pdf(input_pdf_path, output_pdf_path, dados)

# Assinar digitalmente o PDF
sign_pdf(
    pdf_path=output_pdf_path,
    cert_path=cert_path,
    cert_password=cert_password,
    output_path=output_pdf_path,
    field_name='Assinatura Digital'
)
w
print("PDF preenchido e assinado com sucesso!")