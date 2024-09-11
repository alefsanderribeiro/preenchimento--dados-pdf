import pymupdf
from datetime import datetime


class PdfFormFiller:
    def __init__(self, modelo_pdf):
        self.modelo_pdf = modelo_pdf
        self.doc = pymupdf.open(self.modelo_pdf)
        self.page = self.doc[0]
        

    
    def localizar_campo(self, nome_campo):
        return self.page.get_textbox(nome_campo)
        
    def preencher_campo(self, campo, valor):
        for field in self.page.widgets():
            if field.field_name == campo:
                if field.field_type_string == "RadioButton":
                    field.field_value = valor
                    # Ajuste os button_states para corresponder ao formato do Adobe
                    
                    field.button_states = {'normal': [valor, 'Off'], 'down': None}
                else:
                    field.field_value = valor
                field.update()
                print(f"Campo '{campo}' preenchido com valor: {valor}")
                return True
        print(f"Campo '{campo}' não encontrado")
        return False
    
    def todos_campos(self):
        for field in self.page.widgets():
            
            print(field.field_name)
            print(field.on_state())
            print(field.field_value)
            print(field.choice_values)
            
    
    def pesquisar_campo(self, nome_campo):
        for field in self.page.widgets():
            if field.field_name == nome_campo:
                
                print(f"field_name: {field.field_name}")
                print(f"on_state: {field.on_state()}")
                print(f"field_value: {field.field_value}")
                print(f"choice_values: {field.choice_values}")
                print(f"rect: {field.rect}")
                print(f"button_states: {field.button_states()}")
                print(f"field_value == on_state: {field.field_value == field.on_state()}")
                print(f"field_type_string: {field.field_type_string}")
                print(f"field_type: {field.field_type}")
                print(f"field_flags: {field.field_flags}")
                print(f"button_caption: {field.button_caption}")
                print(f"xref: {field.xref}")
                print(f"field_label: {field.field_label}")
                print(f"fill_color: {field.fill_color}")
                print(f"border_color: {field.border_color}")
                print(f"text_color: {field.text_color}")
                print(f"border_width: {field.border_width}")
                print(f"border_style: {field.border_style}")
                print(f"text_font: {field.text_font}")
                print(f"text_fontsize: {field.text_fontsize}")
                print(f"text_maxlen: {field.text_maxlen}")
                print(f"text_format: {field.text_format}")
                print(f"field_display: {field.field_display}")
                
                


            
    
    def preencher_tipo_peticao(self, tipo):
        opcoes = {
            "impugnacao": "0",
            "recurso": "1"
        }
        valor = opcoes.get(tipo, "Off")
        if self.preencher_campo("tipoDaPeticao", valor):
            print(f"Tipo de petição definido como: {tipo}")
        else:
            print("Falha ao preencher o tipo de petição")
            
    def preencher_tipo_atendimento(self, tipo):
        opcoes = {
            "AIH": "aih",
            "APAC": "apac"
        }
        valor = opcoes.get(tipo, "Off")
        if self.preencher_campo("tipoDeAtendimento1", valor):
            print(f"Tipo de atendimento definido como: {tipo}")
        else:
            print("Falha ao preencher o tipo de atendimento")
    # ... (outros métodos de preenchimento permanecem os mesmos)

# Exemplo de uso
if __name__ == "__main__":
    
    #
    print("Primeiro arquivo (Template)")
    form_filler = PdfFormFiller(r"arquivos/modelo_teste.pdf")

    #form_filler.todos_campos()
    
    form_filler.pesquisar_campo("tipoDaPeticao")
    
    form_filler.preencher_tipo_peticao("tipoDeAtendimento1")
    
    form_filler.preencher_tipo_atendimento("AIH")
    
    form_filler.doc.save(r"output/modelo_teste_preenchido.pdf")  # Salva com um nome diferente
    
    
    print( "------------------------------------------" )
    print("Segundo arquivo (Preenchido no Python)")
    form_filler = PdfFormFiller(r"output/modelo_teste_preenchido.pdf")
    
    form_filler.pesquisar_campo("tipoDeAtendimento1")
    
    
    print( "------------------------------------------" )
    print("Terceiro arquivo (Preenchido e Assinado no Adobe)")
    form_filler = PdfFormFiller(r"output/modelo_teste_preenchido2.pdf")
    
    form_filler.pesquisar_campo("tipoDeAtendimento1")
    
    
    print( "------------------------------------------" )
    print("Quarto arquivo (Preenchido e Assinado no Adobe)")
    form_filler = PdfFormFiller(r"output.pdf")
    
    form_filler.pesquisar_campo("tipoDeAtendimento1")
    # Preencher campos
    #form_filler.preencher_tipo_peticao("recurso")
    
    """
    form_filler.preencher_numero_processo("123456")
    form_filler.preencher_numero_atendimento("789012")
    form_filler.preencher_competencia_atendimento("01/2023")
    form_filler.preencher_tipo_atendimento("apac")
    form_filler.preencher_contrato_adaptado(True)
    form_filler.preencher_extensao_area_cobertura_urgencia(False)
    form_filler.preencher_reembolso_urgencia_fora_area(True)
    form_filler.preencher_laudo_auditoria_assistencial(True)
    form_filler.preencher_data_assinatura_contrato(datetime(2023, 1, 1))
    form_filler.preencher_data_adaptacao(datetime(2023, 6, 1))
    form_filler.preencher_numero_clausula_area_geografica("5.1")
    form_filler.preencher_numero_clausula_regulamento_urgencia("7.2")
    form_filler.preencher_numero_prontuario_auditoria("987654")
    form_filler.preencher_informacoes_adicionais("Informações adicionais aqui.")
    """
    # Salvar o PDF preenchido
    #form_filler.salvar_pdf("modelo_teste_preenchido.pdf")

