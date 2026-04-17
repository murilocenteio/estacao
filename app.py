import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configurações de pastas
if not os.path.exists("fotos"):
    os.makedirs("fotos")

DATA_FILE = "dados_estacao.csv"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=['ID', 'Produto', 'Dose', 'Tratamento', 'Repeticao', 'Variavel', 'Valor', 'Data'])

def salvar_dado(df):
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="Gestão Agrícola", layout="wide")
st.sidebar.title("Menu")
menu = st.sidebar.radio("Ir para:", ["Cadastrar", "Coleta", "Ver Dados"])

df_base = carregar_dados()

if menu == "Cadastrar":
    st.header("📝 Cadastro de Experimentos")
    with st.form("cad"):
        prod = st.text_input("Produto")
        dose = st.text_input("Dose")
        trat = st.number_input("Tratamento", min_value=1)
        rep = st.number_input("Repetição", min_value=1)
        if st.form_submit_button("Salvar"):
            novo = pd.DataFrame([[len(df_base)+1, prod, dose, trat, rep, "", 0, datetime.now()]], columns=df_base.columns)
            salvar_dado(pd.concat([df_base, novo], ignore_index=True))
            st.success("Cadastrado!")

elif menu == "Coleta":
    st.header("📸 Coleta e Fotos")
    if not df_base.empty:
        sel_trat = st.selectbox("Tratamento", sorted(df_base['Tratamento'].unique()))
        var = st.text_input("Variável")
        val = st.number_input("Valor")
        foto = st.camera_input("Tirar Foto")
        if st.button("Salvar Coleta"):
            if foto:
                with open(f"fotos/trat_{sel_trat}_{datetime.now().strftime('%H%M%S')}.jpg", "wb") as f:
                    f.write(foto.getbuffer())
            st.success("Dados salvos!")
    else:
        st.info("Cadastre algo primeiro.")

elif menu == "Ver Dados":
    st.header("📊 Dados Acumulados")
    st.dataframe(df_base)
