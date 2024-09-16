from PyPDFForm import FormWrapper, PdfWrapper
from pypdf import PdfReader, PdfWriter
import json
import pandas as pd
from datetime import datetime
from pathlib import Path


from pypdf import PdfReader, PdfWriter
from datetime import datetime


class PdfFormFiller:
    """
    Classe para preencher campos em um formulário PDF.

    A classe permite carregar um modelo PDF e preencher seus campos com dados fornecidos.
    """

    def __init__(self, modelo_pdf):
        """
        Inicializa a classe PdfFormFiller.

        :param modelo_pdf: Caminho para o arquivo PDF modelo.
        """
        self.modelo_pdf = modelo_pdf
        self.reader = PdfReader(self.modelo_pdf)
        self.writer = PdfWriter()
        self.writer.append(self.reader)
        self.num_pages = len(self.reader.pages)

    def preencher_campos(self, campos):
        """
        Preenche os campos do PDF com os dados fornecidos.

        :param campos: Dicionário com os campos e seus respectivos valores.
        """
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
        """
        Salva o PDF preenchido em um novo arquivo.

        :param nome_arquivo: Nome do arquivo de saída.
        """
        with open(nome_arquivo, "wb") as output_stream:
            self.writer.write(output_stream)

    def verificar_campos(self, nome_arquivo):
        """
        Verifica quais campos estão presentes no PDF.

        :param nome_arquivo: Caminho para o arquivo PDF a ser verificado.
        :return: Dicionário com os campos do PDF.
        """
        reader_check = PdfReader(nome_arquivo)
        return reader_check.get_fields()

    def preencher_tipo_peticao(self, tipo):
        """
        Preenche o campo de tipo de petição.

        :param tipo: Tipo de petição (ex: "impugnacao", "recurso").
        """
        opcoes = {
            "impugnacao": "/0",
            "recurso": "/1"
        }
        self.preencher_campos({"tipoDaPeticao": opcoes.get(tipo, "/Off")})

    def preencher_numero_processo(self, numero):
        """
        Preenche o campo de número do processo.

        :param numero: Número do processo a ser preenchido.
        """
        self.preencher_campos({"numeroDoProcesso1": numero})

    def preencher_numero_atendimento(self, numero):
        """
        Preenche o campo de número de atendimento.

        :param numero: Número de atendimento a ser preenchido.
        """
        self.preencher_campos({"numeroDoAtendimento1": numero})

    def preencher_competencia_atendimento(self, competencia):
        """
        Preenche o campo de competência de atendimento.

        :param competencia: Competência a ser preenchida.
        """
        self.preencher_campos({"competenciaDoAtendimento1": competencia})

    def preencher_tipo_atendimento(self, tipo):
        """
        Preenche o campo de tipo de atendimento.

        :param tipo: Tipo de atendimento (ex: "aih", "apac").
        """
        opcoes = {"aih": "aih", "apac": "apac"}
        self.preencher_campos({"tipoDeAtendimento1": opcoes.get(tipo, "null")})

    def preencher_contrato_adaptado(self, adaptado):
        """
        Preenche o campo de contrato adaptado.

        :param adaptado: Booleano indicando se o contrato foi adaptado.
        """
        valor = "/1" if adaptado else "/0"
        self.preencher_campos({"contratoFoiAdaptado": valor})

    def preencher_extensao_area_cobertura_urgencia(self, extensao):
        """
        Preenche o campo de extensão da área de cobertura de urgência.

        :param extensao: Booleano indicando se há extensão.
        """
        valor = "/1" if extensao else "/0"
        self.preencher_campos({"extensaoAreaCoberturaUrgencia": valor})

    def preencher_reembolso_urgencia_fora_area(self, reembolso):
        """
        Preenche o campo de reembolso de urgência fora da área.

        :param reembolso: Booleano indicando se há reembolso.
        """
        valor = "/1" if reembolso else "/0"
        self.preencher_campos({"ReembolsoUrgenciaForaDaAreaCobertura": valor})

    def preencher_laudo_auditoria_assistencial(self, laudo):
        """
        Preenche o campo de laudo de auditoria assistencial.

        :param laudo: Booleano indicando se há laudo.
        """
        valor = "/1" if laudo else "/0"
        self.preencher_campos({"LaudoAuditoriaAssistencialParaAreaDeAbrangenciaGeografica": valor})

    def preencher_data_assinatura_contrato(self, data):
        """
        Preenche o campo de data de assinatura do contrato.

        :param data: Data a ser preenchida.
        """
        self.preencher_campos({"dataAssinaturaContrato": data.strftime("%d/%m/%Y")})

    def preencher_data_adaptacao(self, data):
        """
        Preenche o campo de data de adaptação.

        :param data: Data a ser preenchida.
        """
        self.preencher_campos({"dataDaAdaptacao": data.strftime("%d/%m/%Y")})

    def preencher_numero_clausula_area_geografica(self, numero):
        """
        Preenche o campo de número da cláusula da área geográfica.

        :param numero: Número a ser preenchido.
        """
        self.preencher_campos({"NumeroClausulaAreaGeograficaAbrangencia": numero})

    def preencher_numero_clausula_regulamento_urgencia(self, numero):
        """
        Preenche o campo de número da cláusula do regulamento de urgência.

        :param numero: Número a ser preenchido.
        """
        self.preencher_campos({"NumeroClausulaRegulamentoUrgenciaEmergencia": numero})

    def preencher_numero_prontuario_auditoria(self, numero):
        """
        Preenche o campo de número do prontuário de auditoria.

        :param numero: Número a ser preenchido.
        """
        self.preencher_campos({"NumeroProntuarioAuditoriaAssistencial": numero})

    def preencher_informacoes_adicionais(self, informacoes):
        """
        Preenche o campo de informações adicionais.

        :param informacoes: Informações a serem preenchidas.
        """
        self.preencher_campos({"InformacoesAdicionaisAreaDeAbrangenciaGeografica": informacoes})

    def preencher_assinatura_digital(self, nome_arquivo_saida, certificado_pfx, senha):
        """
        Preenche o campo de assinatura digital (ainda não implementado).

        :param nome_arquivo_saida: Nome do arquivo de saída.
        :param certificado_pfx: Caminho para o certificado PFX.
        :param senha: Senha do certificado.
        """
        # Futuramente ajustar uma assinatura digital
        pass


class FormularioPDF:
    def __init__(self):
        self.modelo_pdf = Path("arquivos\modelo_teste.pdf")
        self.pasta_saida = Path("output").absolute()
        self.FormWrapper = FormWrapper(str(self.modelo_pdf.absolute()))
        self.PdfWrapper = PdfWrapper(str(self.modelo_pdf.absolute()))
        self.caminho_saida = self.pasta_saida / datetime.now().strftime('%d-%m-%Y-%H-%M-%S')

    
    def schema(self):
        """
        Retorna o schema do modelo PDF.

        Este método utiliza o objeto PdfWrapper para obter o schema do modelo PDF
        carregado durante a inicialização da classe. O schema é uma representação
        estruturada dos campos e propriedades do formulário PDF.

        Returns:
            str: Uma string JSON formatada contendo o schema do modelo PDF.
                 O JSON é indentado com 4 espaços e as chaves não são ordenadas
                 alfabeticamente.

        Exemplo de uso:
            formulario = FormularioPDF()
            schema_json = formulario.schema()
            print(schema_json)
        """
        
        return json.dumps(self.PdfWrapper.schema, indent=4, sort_keys=False)
    
    def preview(self):
        preview_stream = self.PdfWrapper.preview
        with open("teste.pdf", "wb+") as output:
            output.write(preview_stream)
    
    def _preencher_formulario(self, dados):
        dados_ajustados = self._ajustar_dados(dados)
        print(dados_ajustados)
        return self.FormWrapper.fill(dados_ajustados, flatten=False, adobe_mode=False)
    
    def _salvar_pdf(self, caminho_arquivo, filled_pdf):
        
        with open(caminho_arquivo, "wb") as output:
            output.write(filled_pdf.read())

    def _ajustar_dados(self, dados):
        dados_ajustados = {}

        # Ajustar tipo de petição
        tipo_peticao = str(dados.get("tipoDaPeticao", "")).lower()
        if "impugnação" in tipo_peticao:
            dados_ajustados["tipoDaPeticao"] = 0
        elif "recurso" in tipo_peticao:
            dados_ajustados["tipoDaPeticao"] = 1
        else:
            dados_ajustados["tipoDaPeticao"] = None

        # Ajustar tipo de atendimento
        tipo_atendimento = str(dados.get("tipoDeAtendimento1", "")).upper()
        if "AIH" in tipo_atendimento:
            dados_ajustados["tipoDeAtendimento1"] = 0
        elif "APAC" in tipo_atendimento:
            dados_ajustados["tipoDeAtendimento1"] = 1
        else:
            dados_ajustados["tipoDeAtendimento1"] = None

        # Ajustar campos booleanos
        campos_booleanos = [
            "contratoFoiAdaptado",
            "extensaoAreaCoberturaUrgencia",
            "ReembolsoUrgenciaForaDaAreaCobertura",
            "LaudoAuditoriaAssistencialParaAreaDeAbrangenciaGeografica"
        ]
        for campo in campos_booleanos:
            if campo in dados:
                valor = str(dados[campo]).upper()
                dados_ajustados[campo] = 1 if valor == 'SIM' else 0

        # Ajustar datas
        campos_data = ["dataAssinaturaContrato", "dataDaAdaptacao"]
        for campo in campos_data:
            if campo in dados and pd.notna(dados[campo]):
                try:
                    if isinstance(dados[campo], pd.Timestamp):
                        data = dados[campo].to_pydatetime()
                    else:
                        data = datetime.strptime(str(dados[campo]), "%Y-%m-%d %H:%M:%S")
                    dados_ajustados[campo] = data.strftime("%d/%m/%Y")
                except ValueError:
                    print(f"Erro ao processar data para o campo {campo}.")
                    dados_ajustados[campo] = ""

        # Ajustar competenciaDoAtendimento1 para mm/aaaa
        if "competenciaDoAtendimento1" in dados and pd.notna(dados["competenciaDoAtendimento1"]):
            try:
                if isinstance(dados["competenciaDoAtendimento1"], pd.Timestamp):
                    data = dados["competenciaDoAtendimento1"].to_pydatetime()
                else:
                    data = datetime.strptime(str(dados["competenciaDoAtendimento1"]), "%Y-%m-%d %H:%M:%S")
                dados_ajustados["competenciaDoAtendimento1"] = data.strftime("%m/%Y")
            except ValueError:
                print("Erro ao processar data para o campo competenciaDoAtendimento1.")
                dados_ajustados["competenciaDoAtendimento1"] = ""

        # Ajustar campos de string
        campos_string = [
            "Assinatura Digital",
            "InformacoesAdicionaisAreaDeAbrangenciaGeografica",
            "NumeroClausulaAreaGeograficaAbrangencia",
            "NumeroClausulaRegulamentoUrgenciaEmergencia",
            "NumeroProntuarioAuditoriaAssistencial",
            "numeroDoAtendimento1",
            "numeroDoProcesso1"
        ]
        for campo in campos_string:
            if campo in dados:
                dados_ajustados[campo] = str(dados[campo]) if pd.notna(dados[campo]) else ""

        return dados_ajustados
    
    def _processar_dados_planilha(self, caminho_planilha):
        # Carregar dados da planilha e converter em um DataFrame do Pandas
        df = pd.read_excel(caminho_planilha)
        ### Executar o processamento da planilha e os devidos ajustes que se fizerem necessários
    
        return df
    def _fazer_ajuste(self, arquivo):

        form_filler = PdfFormFiller(arquivo)

        # Preencher campos
        form_filler.preencher_tipo_atendimento("apac")

        # Salvar o PDF preenchido
        form_filler.salvar_pdf(arquivo)

        
        
    def processar_planilha_em_pdf(self, caminho_planilha):
        """
        Processa uma planilha Excel e gera arquivos PDF individuais para cada linha.

        Este método realiza as seguintes operações:
        1. Verifica e cria a pasta de saída, se necessário.
        2. Processa os dados da planilha usando o método _processar_dados_planilha.
        3. Itera sobre cada linha da planilha processada.
        4. Para cada linha:
           - Converte os dados para um dicionário.
           - Gera um nome de arquivo baseado no número do processo.
           - Preenche um formulário PDF com os dados da linha.
           - Salva o PDF preenchido na pasta de saída.

        Args:
            caminho_planilha (str): Caminho para o arquivo Excel a ser processado.

        Raises:
            FileNotFoundError: Se o arquivo da planilha não for encontrado.
            PermissionError: Se não houver permissão para criar a pasta de saída ou salvar os arquivos.

        Note:
            Este método depende dos métodos _processar_dados_planilha, _preencher_formulario e _salvar_pdf.
        """
        
        # Verificar se o arquivo da planilha existe
        if not Path(caminho_planilha).exists():
            raise FileNotFoundError(f"O arquivo da planilha não foi encontrado: {caminho_planilha}")
        
        try:
            # Criar a pasta de saída se não existir
            if not Path(self.caminho_saida).exists():
                Path(self.caminho_saida).mkdir(parents=True)
        except PermissionError:
            raise PermissionError(f"Sem permissão para criar a pasta de saída: {self.caminho_saida}")
        
        # Processar os dados da planilha
        df = self._processar_dados_planilha(caminho_planilha)
        
        # Iterar sobre as linhas da planilha
        for _, row in df.iterrows():
            # Converter a linha para um dicionário
            dados = row.to_dict()
        
            # Definir nome do arquivo de saída
            nome_arquivo = f"{dados['numeroDoProcesso1']}.pdf"
            caminho_arquivo = self.caminho_saida / nome_arquivo
            
            # Preencher o arquivo PDF
            filled_pdf = self._preencher_formulario(dados)
            
            try:
                # Salvar o arquivo PDF
                self._salvar_pdf(caminho_arquivo, filled_pdf)
                self._fazer_ajuste(caminho_arquivo)
                print(f"PDF gerado: {nome_arquivo}")
            except PermissionError:
                raise PermissionError(f"Sem permissão para salvar o arquivo PDF: {caminho_arquivo}")

# Exemplo de uso
if __name__ == "__main__":
    caminho_planilha = r"arquivos\planilha.xlsx"
    
    PDF = FormularioPDF()
    #print(PDF.schema())
    #PDF.preview()
    
    # Fazer o processamento dos dados da planilha em PDF individual para cada processo
    PDF.processar_planilha_em_pdf(caminho_planilha)
