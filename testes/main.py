from pypdf import PdfReader, PdfWriter
from datetime import datetime


class PdfFormFiller:
    def __init__(self, modelo_pdf):
        self.modelo_pdf = modelo_pdf
        self.reader = PdfReader(self.modelo_pdf)
        self.writer = PdfWriter()
        self.writer.append(self.reader)
        self.num_pages = len(self.reader.pages)

    
    def preencher_campos(self, campos):
        for i in range(self.num_pages):
            try:
                self.writer.update_page_form_field_values(
                page=self.writer.pages[i],
            fields=campos,
            auto_regenerate=True
                )
            except Exception as e:
                print(f"Erro ao preencher o campo {campos} na página {i}: {e}")

    def salvar_pdf(self, nome_arquivo):
        with open(nome_arquivo, "wb") as output_stream:
            self.writer.write(output_stream)

    def verificar_campos(self, nome_arquivo):
        reader_check = PdfReader(nome_arquivo)
        return reader_check.get_fields()

    def preencher_tipo_peticao(self, tipo):
        opcoes = {
            "impugnacao": "/0",
            "recurso": "/1"
        }
        self.preencher_campos({"tipoDaPeticao": opcoes.get(tipo, "/Off")})

    def preencher_numero_processo(self, numero):
        self.preencher_campos({"numeroDoProcesso1": numero})

    def preencher_numero_atendimento(self, numero):
        self.preencher_campos({"numeroDoAtendimento1": numero})

    def preencher_competencia_atendimento(self, competencia):
        self.preencher_campos({"competenciaDoAtendimento1": competencia})

    def preencher_tipo_atendimento(self, tipo):
        opcoes = {"aih": "aih", "apac": "apac"}
        self.preencher_campos({"tipoDeAtendimento1": opcoes.get(tipo, "null")})

    def preencher_contrato_adaptado(self, adaptado):
        valor = "/1" if adaptado else "/0"
        self.preencher_campos({"contratoFoiAdaptado": valor})

    def preencher_extensao_area_cobertura_urgencia(self, extensao):
        valor = "/1" if extensao else "/0"
        self.preencher_campos({"extensaoAreaCoberturaUrgencia": valor})

    def preencher_reembolso_urgencia_fora_area(self, reembolso):
        valor = "/1" if reembolso else "/0"
        self.preencher_campos({"ReembolsoUrgenciaForaDaAreaCobertura": valor})

    def preencher_laudo_auditoria_assistencial(self, laudo):
        valor = "/1" if laudo else "/0"
        self.preencher_campos({"LaudoAuditoriaAssistencialParaAreaDeAbrangenciaGeografica": valor})

    def preencher_data_assinatura_contrato(self, data):
        self.preencher_campos({"dataAssinaturaContrato": data.strftime("%d/%m/%Y")})

    def preencher_data_adaptacao(self, data):
        self.preencher_campos({"dataDaAdaptacao": data.strftime("%d/%m/%Y")})

    def preencher_numero_clausula_area_geografica(self, numero):
        self.preencher_campos({"NumeroClausulaAreaGeograficaAbrangencia": numero})

    def preencher_numero_clausula_regulamento_urgencia(self, numero):
        self.preencher_campos({"NumeroClausulaRegulamentoUrgenciaEmergencia": numero})

    def preencher_numero_prontuario_auditoria(self, numero):
        self.preencher_campos({"NumeroProntuarioAuditoriaAssistencial": numero})

    def preencher_informacoes_adicionais(self, informacoes):
        self.preencher_campos({"InformacoesAdicionaisAreaDeAbrangenciaGeografica": informacoes})

    # Novo método para o campo de assinatura digital
    ## Preciso verificar como fazer para o campo de assinatura digital
    def preencher_assinatura_digital(self, nome_arquivo_saida, certificado_pfx, senha):
        # Futuramente ajustar uma assinatura digita
        pass
        
    

# Exemplo de uso
if __name__ == "__main__":
    form_filler = PdfFormFiller(r"arquivos/modelo_teste.pdf")
    
    
    # Preencher campos
    
    form_filler.preencher_tipo_atendimento("apac")
    form_filler.preencher_tipo_peticao("impugnacao")

    
    # Salvar o PDF preenchido
    form_filler.salvar_pdf(r"output\testes_preenc_adobe.pdf")
    
