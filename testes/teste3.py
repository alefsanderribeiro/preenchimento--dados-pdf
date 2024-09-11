from pypdf import PdfReader, PdfWriter

reader = PdfReader("modelo.pdf")
writer = PdfWriter()

page = reader.pages[0]
fields = reader.get_fields()
print(fields)

writer.append(reader)
writer._update_field_annotation
writer.update_page_form_field_values(
    writer.pages[0],
    {"tipoDaPeticao":"/1", "tipoDeAtendimento1":"apac", "contratoFoiAdaptado":"/1"},
    auto_regenerate=True,
)

with open("filled-out.pdf", "wb") as output_stream:
    writer.write(output_stream)

# Verificar se o campo foi preenchido corretamente
reader_check = PdfReader("filled-out.pdf")
fields_check = reader_check.get_fields()
print(fields_check['tipoDaPeticao'])