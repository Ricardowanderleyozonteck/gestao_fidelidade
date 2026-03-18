import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def mostrar_dashboard(conn):

    st.title("📊 Gestão de Consultores")

    df = pd.read_sql("SELECT * FROM ciclos ORDER BY ciclo", conn)

    if df.empty:
        st.warning("Nenhum dado disponível.")
        return

    busca = st.text_input("🔎 Buscar consultor")

    resultado = {}
    ciclos = sorted(df["ciclo"].unique())

    for ciclo in ciclos:

        dados_ciclo = df[df["ciclo"] == ciclo]
        nomes_ciclo = set(dados_ciclo["nome"])

        # 🔴 AUSENTES
        for nome in list(resultado.keys()):
            if nome not in nomes_ciclo:

                r = resultado[nome]

                if r["status"] in ["Novo", "Ativo"]:
                    r["status"] = "Inativo"
                    r["inativo"] = 1
                else:
                    if r["inativo"] == 1:
                        r["status"] = "Excluído"
                    else:
                        r["inativo"] += 1

                r["valor"] = 0

        # 🟢 PRESENTES
        for _, row in dados_ciclo.iterrows():

            nome = row["nome"]
            valor = row["valor"]

            if nome not in resultado:
                resultado[nome] = {
                    "total": 0,
                    "meses": 0,
                    "status": "Novo",
                    "inativo": 0,
                    "valor": 0
                }

            r = resultado[nome]

            # 🟢 ATIVO
            if r["status"] in ["Novo", "Ativo"]:

                if valor >= 150:
                    r["total"] += valor
                    r["meses"] += 1
                    r["status"] = "Ativo"
                    r["inativo"] = 0
                else:
                    r["status"] = "Inativo"
                    r["inativo"] = 1

            # 🔴 INATIVO
            else:

                if r["inativo"] == 1:

                    if valor >= 300:
                        r["total"] += valor
                        r["meses"] += 1

                    elif valor >= 150:
                        r["total"] = valor
                        r["meses"] = 1

                    if valor >= 150:
                        r["status"] = "Ativo"
                        r["inativo"] = 0
                    else:
                        r["status"] = "Excluído"

                else:
                    if valor >= 150:
                        r["total"] = valor
                        r["meses"] = 1
                        r["status"] = "Ativo"
                        r["inativo"] = 0
                    else:
                        r["status"] = "Excluído"

            r["valor"] = valor

    # 📋 TABELA FINAL
    dados = []

    for nome, r in resultado.items():
        if r["status"] != "Excluído":

            if busca and busca.upper() not in nome:
                continue

            dados.append([
                nome,
                r["valor"],
                r["total"],
                r["meses"],
                r["status"]
            ])

    df_final = pd.DataFrame(dados, columns=[
        "Consultor", "Valor Ciclo", "Valor Total", "Meses", "Status"
    ])

    st.dataframe(df_final, use_container_width=True)

    # 📥 EXPORTAR
    csv = df_final.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar Relatório", csv, "relatorio.csv", "text/csv")

    # 🏆 RANKING POR VALOR
    st.subheader("🏆 Top 10 Consultores (Valor Total)")
    ranking = df_final.sort_values(by="Valor Total", ascending=False).head(10)
    st.dataframe(ranking, use_container_width=True)

    # 📊 GRÁFICO VALOR
    st.subheader("📊 Ranking por Valor")
    plt.figure()
    plt.barh(ranking["Consultor"], ranking["Valor Total"])
    st.pyplot(plt)

    # 🏅 RANKING POR TEMPO ATIVO
    st.subheader("🏅 Top 10 Mais Tempo Ativo (Somente Ativos)")

    ativos = df_final[df_final["Status"] == "Ativo"]
    ranking_tempo = ativos.sort_values(by="Meses", ascending=False).head(10)

    st.dataframe(ranking_tempo, use_container_width=True)

    # 📊 GRÁFICO TEMPO
    st.subheader("📊 Ranking por Tempo Ativo")
    plt.figure()
    plt.barh(ranking_tempo["Consultor"], ranking_tempo["Meses"])
    st.pyplot(plt)

    # 📈 EVOLUÇÃO INDIVIDUAL
    st.subheader("📈 Evolução por Consultor")

    df_grafico = pd.read_sql("SELECT nome, ciclo, valor FROM ciclos", conn)

    consultor = st.selectbox("Selecionar consultor", df_grafico["nome"].unique())

    dados_consultor = df_grafico[df_grafico["nome"] == consultor]

    plt.figure()
    plt.plot(dados_consultor["ciclo"], dados_consultor["valor"], marker='o')
    plt.xlabel("Ciclo")
    plt.ylabel("Valor")
    plt.title(f"Evolução - {consultor}")

    st.pyplot(plt)