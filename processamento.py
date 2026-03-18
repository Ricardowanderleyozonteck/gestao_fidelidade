import pandas as pd
import streamlit as st
from utils import normalizar_nome, normalizar_valor

def processar_planilha(conn, arquivo):

    cursor = conn.cursor()
    nome_arquivo = arquivo.name

    cursor.execute("SELECT 1 FROM arquivos_processados WHERE nome_arquivo=?", (nome_arquivo,))
    if cursor.fetchone():
        st.warning("⚠️ Arquivo já processado.")
        return

    df = pd.read_excel(arquivo)
    df.columns = df.columns.str.strip()

    if "Cliente" not in df.columns or "Valor" not in df.columns:
        st.error("❌ Planilha precisa ter colunas: Cliente e Valor")
        return

    df = df[["Cliente", "Valor"]].dropna()

    df["Cliente"] = df["Cliente"].apply(normalizar_nome)
    df["Valor"] = df["Valor"].apply(normalizar_valor)

    df = df.groupby("Cliente", as_index=False)["Valor"].sum()

    cursor.execute("SELECT MAX(ciclo) FROM ciclos")
    ciclo = (cursor.fetchone()[0] or 0) + 1

    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO ciclos (nome, ciclo, valor) VALUES (?, ?, ?)",
            (row["Cliente"], ciclo, row["Valor"])
        )

    cursor.execute("INSERT INTO arquivos_processados VALUES (?)", (nome_arquivo,))
    conn.commit()

    st.success(f"✅ Ciclo {ciclo} processado com sucesso!")