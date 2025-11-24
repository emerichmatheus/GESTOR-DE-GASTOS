import logging
import pandas as pd

logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Iniciando o sistema de controle financeiro - Parte 4")


arquivo = r"C:\Users\Matheus Emerich\OneDrive\TRABALHO BFJ\TRABALHO PYTHON.xlsx"

try:
    df = pd.read_excel(arquivo, sheet_name="Transacoes")
    logging.info("Planilha carregada com sucesso. Linhas: %d", len(df))
except Exception as erro:
    logging.error("Erro ao carregar o arquivo: %s", erro)
    exit()

try:
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Data"])
    logging.info("Datas tratadas. Linhas válidas: %d", len(df))
except Exception as erro:
    logging.error("Erro ao tratar datas: %s", erro)


try:
    df["Tipo"] = df["Tipo"].str.lower().str.strip()

    receitas = df[df["Tipo"].isin(["entrada", "receita"])]
    despesas = df[df["Tipo"].isin(["saida", "despesa", "gasto"])]

    logging.info("Receitas encontradas: %d", len(receitas))
    logging.info("Despesas encontradas: %d", len(despesas))
except Exception as erro:
    logging.error("Erro ao separar receitas e despesas: %s", erro)


try:
    total_receitas = receitas["Valor"].sum()
    total_despesas = despesas["Valor"].sum()
    saldo = total_receitas - total_despesas

    logging.info("Total de receitas: %.2f", total_receitas)
    logging.info("Total de despesas: %.2f", total_despesas)
    logging.info("Saldo final: %.2f", saldo)

    print("Cálculos realizados! Veja o arquivo log.txt para detalhes.")
except Exception as erro:
    logging.error("Erro ao calcular totais: %s", erro)

logging.info("Sistema finalizado.")
