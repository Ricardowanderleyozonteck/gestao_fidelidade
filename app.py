import streamlit as st
from banco import conectar
from processamento import processar_planilha
from dashboard import mostrar_dashboard

st.set_page_config(
    page_title="Sistema Fidelidade",
    layout="wide"
)

conn = conectar()

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}
.big-title {
    font-size:32px;
    font-weight:bold;
    color:#4CAF50;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 Sistema de Fidelidade</div>', unsafe_allow_html=True)

menu = st.sidebar.radio("Menu", ["📥 Upload", "📊 Dashboard", "🧹 Reset"])

if menu == "📥 Upload":

    st.subheader("📥 Enviar Planilha")
    arquivo = st.file_uploader("Selecione o arquivo Excel")

    if arquivo:
        processar_planilha(conn, arquivo)

elif menu == "📊 Dashboard":

    mostrar_dashboard(conn)

elif menu == "🧹 Reset":

    if st.button("⚠️ Resetar Banco"):
        conn.execute("DELETE FROM ciclos")
        conn.execute("DELETE FROM arquivos_processados")
        conn.commit()
        st.success("Banco resetado!")