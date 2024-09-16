from fillpdf import fillpdfs
import pandas as pd
from pathlib import Path
import numpy as np
from datetime import datetime

class FormularioPDF:
    def __init__(self):
        self.modelo_pdf = Path(r"arquivos\modelo_teste.pdf")
        self.pasta_saida = Path("output").absolute()
        
        
    def verificar_dados(self):
        return fillpdfs.get_form_fields(self.modelo_pdf)

    def _ajustar_dados(self, dados):
        dados_ajustados = {}
        
        # Ajustar tipo de petição
        tipo_peticao = str(dados.get("tipoDaPeticao", "")).lower()
        if "impugnação" in tipo_peticao:
            dados_ajustados["tipoDaPeticao"] = "0"  # Radio group
        elif "recurso" in tipo_peticao:
            dados_ajustados["tipoDaPeticao"] = "1"  # Radio group
        else:
            dados_ajustados["tipoDaPeticao"] = "2"  # Default option

        # Ajustar checkboxes e radio boxes
        dados_ajustados["contratoFoiAdaptado"] = "1" if dados.get("contratoFoiAdaptado") == "SIM" else "0"
        dados_ajustados["extensaoAreaCoberturaUrgencia"] = "1" if dados.get("extensaoAreaCoberturaUrgencia") == "SIM" else "0"
        dados_ajustados["ReembolsoUrgenciaForaDaAreaCobertura"] = "1" if dados.get("ReembolsoUrgenciaForaDaAreaCobertura") == "SIM" else "0"
        dados_ajustados["LaudoAuditoriaAssistencialParaAreaDeAbrangenciaGeografica"] = "1" if dados.get("LaudoAuditoriaAssistencialParaAreaDeAbrangenciaGeografica") == "SIM" else "0"

        # Ajustar dropdowns
        if dados.get("tipoDeAtendimento1") == "AIH":
            dados_ajustados["tipoDeAtendimento1"] = "aih"

        elif dados.get("tipoDeAtendimento1") == "APAC":
            dados_ajustados["tipoDeAtendimento1"] = "apac" 
            
        else:
            dados_ajustados["tipoDeAtendimento1"] ="null"
            
        
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

    def processar_planilha_em_pdf(self, caminho_planilha):
        df = pd.read_excel(caminho_planilha)
        for _, row in df.iterrows():
            dados = row.to_dict()
            dados_ajustados = self._ajustar_dados(dados)

            # Definir nome do arquivo de saída
            nome_arquivo = f"{dados['numeroDoProcesso1']}.pdf"
            caminho_arquivo = self.pasta_saida / nome_arquivo
            
            # Preencher o PDF
            fillpdfs.write_fillable_pdf(str(self.modelo_pdf), str(caminho_arquivo), dados_ajustados)
            print(f"PDF gerado: {nome_arquivo}")

# Exemplo de uso
if __name__ == "__main__":
    caminho_planilha = r"arquivos\planilha.xlsx"
    
    PDF = FormularioPDF()
    PDF.processar_planilha_em_pdf(caminho_planilha)
