import os
import pandas as pd
from datetime import datetime

ARQUIVO = r"C:\Users\Matheus Emerich\OneDrive\TRABALHO BFJ\TRABALHO PYTHON.xlsx"
ABA = "Transacoes"
COLUNAS = ["Data", "Tipo", "Categoria", "Descricao", "Valor"]


def carregar_dados():
    # Se o arquivo não existir, cria com a aba correta
    if not os.path.exists(ARQUIVO):
        df = pd.DataFrame(columns=COLUNAS)
        df.to_excel(ARQUIVO, sheet_name=ABA, index=False)
        return df

    try:
        df = pd.read_excel(ARQUIVO, sheet_name=ABA)
        return df
    except Exception:
        print("\n⚠ A aba 'Transacoes' não existe. Criando agora...\n")
        df = pd.DataFrame(columns=COLUNAS)
        df.to_excel(ARQUIVO, sheet_name=ABA, index=False)
        return df


def salvar_dados(df):
    try:
        df.to_excel(ARQUIVO, sheet_name=ABA, index=False)
    except PermissionError:
        print("\n ERRO: Não foi possível salvar o arquivo.")
        print("➡ Feche o Excel ou pause a sincronização do OneDrive e tente novamente.\n")


def ler_data(mensagem="Data (dd/mm/aaaa): "):
    while True:
        entrada = input(mensagem)
        try:
            dt = datetime.strptime(entrada, "%d/%m/%Y")
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            print("Data inválida! Tente no formato dd/mm/aaaa.")


def ler_tipo():
    while True:
        t = input("Tipo (entrada/saida): ").lower()
        if t in ["entrada", "e"]:
            return "entrada"
        elif t in ["saida", "saída", "s"]:
            return "saida"
        print("Tipo inválido!")


def ler_valor():
    while True:
        v = input("Valor: ").replace(",", ".")
        try:
            return float(v)
        except ValueError:
            print("Valor inválido.")

def adicionar(df):
    print("\n--- Adicionar Transação ---")
    data = ler_data()
    tipo = ler_tipo()
    cat = input("Categoria: ")
    desc = input("Descrição: ")
    valor = ler_valor()

    nova = {
        "Data": data,
        "Tipo": tipo,
        "Categoria": cat,
        "Descricao": desc,
        "Valor": valor
    }

    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
    salvar_dados(df)
    print("✓ Transação adicionada!\n")
    return df


def remover(df):
    print("\n--- Remover Transação ---")
    if df.empty:
        print("Nenhuma transação cadastrada.\n")
        return df

    print(df.reset_index(drop=False))

    while True:
        try:
            idx = int(input("ID para remover: "))
            df = df.drop(index=idx)
            df = df.reset_index(drop=True)
            salvar_dados(df)
            print("✓ Removido!\n")
            return df
        except:
            print("ID inválido!")


def listar_cat(df):
    cat = input("\nCategoria: ").lower()
    filtrado = df[df["Categoria"].str.lower() == cat]

    if filtrado.empty:
        print("Nenhuma transação nessa categoria.\n")
    else:
        print(filtrado)
        print()


def listar_periodo(df):
    print("\n--- Período ---")
    ini = ler_data("Data inicial: ")
    fim = ler_data("Data final: ")

    d1 = datetime.strptime(ini, "%d/%m/%Y")
    d2 = datetime.strptime(fim, "%d/%m/%Y")

    temp = df.copy()
    temp["Data_dt"] = pd.to_datetime(temp["Data"], format="%d/%m/%Y")

    filtrado = temp[(temp["Data_dt"] >= d1) & (temp["Data_dt"] <= d2)]

    print(filtrado.drop(columns="Data_dt"))
    print()


def saldo_periodo(df):
    print("\n--- Saldo por período ---")
    ini = ler_data("Data inicial: ")
    fim = ler_data("Data final: ")

    d1 = datetime.strptime(ini, "%d/%m/%Y")
    d2 = datetime.strptime(fim, "%d/%m/%Y")

    temp = df.copy()
    temp["Data_dt"] = pd.to_datetime(temp["Data"], format="%d/%m/%Y")

    filtrado = temp[(temp["Data_dt"] >= d1) & (temp["Data_dt"] <= d2)]

    if filtrado.empty:
        print("Nenhuma transação.\n")
        return

    def aplicar_sinal(linha):
        return linha["Valor"] if linha["Tipo"] == "entrada" else -linha["Valor"]

    valores = filtrado.apply(aplicar_sinal, axis=1)
    saldo = valores.sum()

    print("\nTransações:")
    print(filtrado.drop(columns="Data_dt"))
    print(f"\n➡ Saldo do período: R$ {saldo:.2f}\n")

def menu():
    df = carregar_dados()

    while True:
        print("=== SISTEMA FINANCEIRO ===")
        print("1 - Adicionar transação")
        print("2 - Remover transação")
        print("3 - Listar por categoria")
        print("4 - Listar por período")
        print("5 - Saldo por período")
        print("6 - Sair")

        op = input("Opção: ")

        if op == "1":
            df = adicionar(df)
        elif op == "2":
            df = remover(df)
        elif op == "3":
            listar_cat(df)
        elif op == "4":
            listar_periodo(df)
        elif op == "5":
            saldo_periodo(df)
        elif op == "6":
            print("Encerrando...")
            break
        else:
            print("Opção inválida!\n")


if __name__ == "__main__":
    menu()
