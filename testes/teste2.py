from pypdf import PdfReader

reader = PdfReader("modelo.pdf")
fields = reader.get_form_text_fields()

# You can also get all fields:
#fields = reader.get_fields()

print(fields)



fields3 = reader.get_fields()

print(fields3)