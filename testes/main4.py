from PyPDFForm import FormWrapper, PdfWrapper
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

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
                print(f"PDF gerado: {nome_arquivo}")
            except PermissionError:
                raise PermissionError(f"Sem permissão para salvar o arquivo PDF: {caminho_arquivo}")

# Exemplo de uso
if __name__ == "__main__":
    caminho_planilha = r"arquivos\planilha.xlsx"
    
    PDF = FormularioPDF()
    print(PDF.schema())
    #PDF.preview()
    
    
    # Fazer o processamento dos dados da planilha em PDF individual para cada processo
    PDF.processar_planilha_em_pdf(caminho_planilha)
