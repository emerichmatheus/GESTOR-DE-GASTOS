import pandas as pd
import matplotlib.pyplot as plt

arquivo_excel = r"C:\Users\Matheus Emerich\OneDrive\TRABALHO BFJ\TRABALHO PYTHON.xlsx"


df = pd.read_excel(arquivo_excel, sheet_name="Transacoes")

# Esperado na planilha:
# Colunas: Data | Tipo | Categoria | Descricao | Valor


def parse_data(valor):
    s = str(valor).strip()
    if not s:
        return pd.NaT

    digits = ''.join(ch for ch in s if ch.isdigit())
    if len(digits) == 8:

        return pd.to_datetime(digits, format="%d%m%Y", errors="coerce")

    return pd.to_datetime(s, dayfirst=True, errors="coerce")

df["Data"] = df["Data"].map(parse_data)


df = df.dropna(subset=["Data"])


tipo_lower = df["Tipo"].astype(str).str.lower().str.strip()

mask_receita = tipo_lower.isin(["entrada", "receita"])
mask_despesa = tipo_lower.isin(["saida", "despesa", "gasto"])


total_receitas = df.loc[mask_receita, "Valor"].sum()
total_despesas = df.loc[mask_despesa, "Valor"].sum()
saldo_final = total_receitas - total_despesas

print("===== TOTAL NO PERÍODO =====")
print(f"Total de Receitas: R$ {total_receitas:.2f}")
print(f"Total de Despesas: R$ {total_despesas:.2f}")
print(f"Saldo Final:       R$ {saldo_final:.2f}")
print()


df["AnoMes"] = df["Data"].dt.to_period("M")


mensal = df.groupby(["AnoMes", tipo_lower])["Valor"].sum().unstack().fillna(0)

for col in ["entrada", "receita", "saida", "despesa", "gasto"]:
    if col not in mensal.columns:
        mensal[col] = 0


mensal["Receitas"] = mensal["entrada"] + mensal["receita"]
# despesas = saída + despesa + gasto
mensal["Despesas"] = mensal["saida"] + mensal["despesa"] + mensal["gasto"]
mensal["Saldo"] = mensal["Receitas"] - mensal["Despesas"]

print("===== SALDO MENSAL =====")
print(mensal[["Receitas", "Despesas", "Saldo"]])
print()


df_despesas = df.loc[mask_despesa].copy()

if not df_despesas.empty:
    media_gastos_cat = df_despesas.groupby("Categoria")["Valor"].mean()
    print("===== MÉDIA DE GASTOS POR CATEGORIA =====")
    print(media_gastos_cat)
    print()
else:
    print("Não há despesas cadastradas para calcular média por categoria.\n")


if not df_despesas.empty:
    gastos_categoria = df_despesas.groupby("Categoria")["Valor"].sum()

    plt.figure(figsize=(7, 7))
    plt.pie(gastos_categoria,
            labels=gastos_categoria.index,
            autopct="%1.1f%%")
    plt.title("Proporção dos Gastos por Categoria")
    plt.tight_layout()
    plt.show()


df_sorted = df.sort_values("Data").copy()


def ajusta_sinal(linha):
    t = str(linha["Tipo"]).lower().strip()
    if t in ["entrada", "receita"]:
        return linha["Valor"]
    elif t in ["saida", "despesa", "gasto"]:
        return -linha["Valor"]
    else:

        return 0

df_sorted["ValorAjustado"] = df_sorted.apply(ajusta_sinal, axis=1)
df_sorted["SaldoAcumulado"] = df_sorted["ValorAjustado"].cumsum()

plt.figure(figsize=(10, 5))
plt.plot(df_sorted["Data"], df_sorted["SaldoAcumulado"], marker="o")
plt.title("Saldo Acumulado ao Longo do Tempo")
plt.xlabel("Data")
plt.ylabel("Saldo Acumulado (R$)")
plt.grid(True)
plt.tight_layout()
plt.show()
