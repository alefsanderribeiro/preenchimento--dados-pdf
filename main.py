from PyPDFForm import FormWrapper, PdfWrapper
from pathlib import Path
import json
import pandas as pd
from datetime import datetime
import unicodedata
import re

# TODO: Você pode usar o TK-Inter pra fazer uma GUI pra facilitar a utilização.
# https://www.devmedia.com.br/tkinter-interfaces-graficas-em-python/33956
# Se precisar de ajuda pode me gritar!
# -----------------------------------------
# Fiz alterações diretas no modelo dos forms no PDF, pois a Adobe é bem chatinha com algumas
# coisas tipo botões, radial, check e etc...

class FormularioPDF:
    def __init__(self):
        self.modelo_pdf = Path(r"arquivos\modelo_teste.pdf")  # Define o caminho do modelo PDF
        self.pasta_saida = Path("output").absolute()  # Define o diretório de saída absoluto
        self.FormWrapper = FormWrapper(str(self.modelo_pdf.absolute()))  # Inicializa o FormWrapper com o modelo PDF
        self.PdfWrapper = PdfWrapper(str(self.modelo_pdf.absolute()))  # Inicializa o PdfWrapper com o modelo PDF
        self.caminho_saida = self.pasta_saida / datetime.now().strftime('%d-%m-%Y-%H-%M-%S')  # Define o caminho de saída com timestamp

    # TODO: Dar finalidade a função não utilizada
    def schema(self):
        """
        Retorna o esquema do formulário PDF em formato JSON.
        """
        return json.dumps(self.PdfWrapper.schema, indent=4, sort_keys=False)  # Converte o esquema para JSON formatado

    # TODO: Dar finalidade a função não utilizada
    def preview(self):
        """
        Gera uma visualização do formulário PDF e salva em um arquivo.
        """
        preview_stream = self.PdfWrapper.preview  # Obtém o fluxo de visualização do formulário
        with open("teste.pdf", "wb+") as output:
            output.write(preview_stream)  # Salva a visualização em um arquivo PDF

    

    def _preencher_formulario(self, dados):
        """
        Preenche o formulário PDF com os dados fornecidos.
        """
        dados_ajustados = self._ajustar_dados(dados)  # Ajusta os dados conforme a necessidade do formulário
        print(dados_ajustados)  # Exibe os dados ajustados
        # Preenche o formulário com os dados ajustados, achatando os campos para garantir que as alterações sejam visíveis
        return self.FormWrapper.fill(dados_ajustados, flatten=True, adobe_mode=True)

    def _salvar_pdf(self, caminho_arquivo, filled_pdf):
        """
        Salva o PDF preenchido em um arquivo.
        """
        with open(caminho_arquivo, "wb") as output:
            output.write(filled_pdf.read())  # Salva o conteúdo do PDF preenchido no arquivo especificado
            
            
    def _remover_acentos(self, texto):
        nfkd = unicodedata.normalize('NFKD', texto)
        texto_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
        texto_sem_acento = re.sub(r'ç', 'c', texto_sem_acento)
        return texto_sem_acento

    def _ajustar_dados(self, dados):
        """
        Ajusta os dados fornecidos para corresponder aos campos do formulário PDF.
        """
        dados_ajustados = {}
        self._ajustar_tipo_peticao(dados, dados_ajustados)
        self._ajustar_campos_booleanos(dados, dados_ajustados)
        self._ajustar_datas(dados, dados_ajustados)
        self._ajustar_campos_string(dados, dados_ajustados)
        self._ajustar_tipo_atendimento(dados, dados_ajustados)
        self._ajustar_data_adaptacao(dados, dados_ajustados)
        return dados_ajustados  # Retorna os dados ajustados para preencher o formulário

    def _ajustar_tipo_peticao(self, dados, dados_ajustados):
        """
        Ajusta o tipo de petição e preenche os campos específicos.
        """
        tipo_peticao = str(dados.get("tipoDaPeticao", "")).lower()
                
        sanitize_peticao = self._remover_acentos(tipo_peticao)


        if "impugnacao" in sanitize_peticao:
            dados_ajustados["tipoDaPeticaoImpug"] = "6"
            dados_ajustados["tipoDaPeticaoRecur"] = ""
        elif "recurso" in sanitize_peticao:
            dados_ajustados["tipoDaPeticaoImpug"] = ""
            dados_ajustados["tipoDaPeticaoRecur"] = "6"
        else:
            dados_ajustados["tipoDaPeticaoImpug"] = ""
            dados_ajustados["tipoDaPeticaoRecur"] = ""

    def _ajustar_campos_booleanos(self, dados, dados_ajustados):
        """
        Ajusta os campos booleanos de acordo com os valores fornecidos.
        """
        campos_booleanos = [
            "contratoFoiAdaptado",
            "extensaoAreaCoberturaUrgencia",
            "ReembolsoUrgenciaForaDaAreaCobertura",
            "LaudoAuditoriaAssistencialParaAreaDeAbrangenciaGeografica"
        ]

        for campo in campos_booleanos:
            if campo in dados:
                valor = str(dados[campo]).upper()
                if valor == 'SIM':
                    dados_ajustados[f"{campo}True"] = "6"
                    dados_ajustados[f"{campo}False"] = ""
                else:
                    dados_ajustados[f"{campo}True"] = ""
                    dados_ajustados[f"{campo}False"] = "6"
            else:
                dados_ajustados[f"{campo}True"] = ""
                dados_ajustados[f"{campo}False"] = ""

    def _ajustar_datas(self, dados, dados_ajustados):
        """
        Ajusta os campos de data para o formato adequado.
        """
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

    def _ajustar_tipo_atendimento(self, dados, dados_ajustados):
        """
        Ajusta o campo de tipo de atendimento.
        """
        try:
            tipo = dados.get("tipoDeAtendimento1", "")

            # Verifica se tipo é uma lista ou tupla e extrai o primeiro item
            if isinstance(tipo, (list, tuple)):
                tipo = tipo[0] if tipo else ""
            elif isinstance(tipo, (str, bytes)):
                tipo = tipo
            else:
                tipo = ""

            tipo = str(tipo).strip().lower()
            # print(f"Tipo de Atendimento Original: {tipo}")  # Debug

            opcoes = {"aih": "AIH", "apac": "APAC"}
            tipo_formatado = opcoes.get(tipo, "")
            # print(f"Tipo de Atendimento Formatado: {tipo_formatado}")  # Debug

            dados_ajustados["tipoDeAtendimento1"] = tipo_formatado
        except Exception as e:
            print(f"Erro ao ajustar tipo de atendimento: {e}")

    def _ajustar_data_adaptacao(self, dados, dados_ajustados):
        """
        Ajusta o campo de data de adaptação.

        :param dados: Dados originais do formulário.
        :param dados_ajustados: Dados ajustados para o formulário.
        """
        data = dados.get("dataDaAdaptacao")
        if pd.notna(data):
            try:
                if isinstance(data, pd.Timestamp):
                    data = data.to_pydatetime()
                else:
                    data = datetime.strptime(str(data), "%Y-%m-%d %H:%M:%S")
                dados_ajustados["dataDaAdaptacao"] = data.strftime("%d/%m/%Y")
            except ValueError:
                print(f"Erro ao processar data para o campo dataDaAdaptacao.")
                dados_ajustados["dataDaAdaptacao"] = ""
        else:
            dados_ajustados["dataDaAdaptacao"] = ""

    def _ajustar_campos_string(self, dados, dados_ajustados):
        """
        Ajusta os campos de string de acordo com os valores fornecidos.
        """
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

    def _processar_dados_planilha(self, caminho_planilha):
        """
        Processa uma planilha Excel e retorna os dados em um DataFrame.
        """
        return pd.read_excel(caminho_planilha)  # Lê os dados da planilha Excel em um DataFrame

    def processar_planilha_em_pdf(self, caminho_planilha):
        """
        Processa uma planilha Excel e preenche o formulário PDF com os dados.
        """
        if not Path(caminho_planilha).exists():
            raise FileNotFoundError(f"O arquivo da planilha não foi encontrado: {caminho_planilha}")

        try:
            if not Path(self.caminho_saida).exists():
                Path(self.caminho_saida).mkdir(parents=True)  # Cria o diretório de saída se não existir

            df = self._processar_dados_planilha(caminho_planilha)  # Processa a planilha e obtém os dados
            for _, linha in df.iterrows():
                dados = linha.to_dict()  # Converte cada linha em um dicionário
                pdf_preenchido = self._preencher_formulario(dados)  # Preenche o formulário com os dados
                caminho_arquivo = self.caminho_saida / f"{dados['numeroDoProcesso1']}.pdf"  # Define o caminho do arquivo PDF
                self._salvar_pdf(caminho_arquivo, pdf_preenchido)  # Salva o PDF preenchido no arquivo especificado

        except Exception as e:
            print(f"Erro ao processar a planilha: {e}")  # Captura e exibe qualquer exceção ocorrida


if __name__ == "__main__":
    formulario = FormularioPDF()
    caminho_planilha = r"arquivos\planilha.xlsx"  # Defina o caminho da planilha
    formulario.processar_planilha_em_pdf(caminho_planilha)  # Processa a planilha e gera os PDFs
