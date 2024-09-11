from pypdf import PdfReader, PdfWriter

reader = PdfReader("modelo_teste.pdf")
writer = PdfWriter()

page = reader.pages[0]
fields = reader.get_fields()
print(fields)

writer.append(reader)
writer._update_field_annotation
writer.update_page_form_field_values(
    writer.pages[0],
    {"tipoDaPeticao":"/0"},
    auto_regenerate=True,
)

with open("filled-out_teste.pdf", "wb") as output_stream:
    writer.write(output_stream)

# Verificar se o campo foi preenchido corretamente
reader_check = PdfReader("filled-out_teste.pdf")
fields_check = reader_check.get_fields()
print(fields_check['tipoDaPeticao'])





def preencher_tipo_peticao(tipo):
        opcoes = {
            "impugnacao": "/0",
            "recurso": "/1"
        }
        res = {"tipoDaPeticao": opcoes.get(tipo, "/Off")}
        return res


print(preencher_tipo_peticao("impugnacao"))


