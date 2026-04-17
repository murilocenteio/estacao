import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração de persistência simples
DATA_FILE = "dados_estacao_v2.csv"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=[
        'Experimento', 'Tratamento', 'Descricao_Trat', 'Repeticao', 'Variavel', 'Valor', 'Data'
    ])

def salvar_dado(df):
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="BioField Pro", layout="wide")
df_base = carregar_dados()

st.sidebar.title("🌱 Estação Experimental")
menu = st.sidebar.radio("Navegação", ["1. Configurar Experimento", "2. Coleta de Campo", "3. Exportar Relatório"])

# --- 1. CONFIGURAR EXPERIMENTO ---
if menu == "1. Configurar Experimento":
    st.header("🔬 Novo Delineamento")
    
    with st.expander("Clique para cadastrar um novo experimento", expanded=True):
        nome_exp = st.text_input("Nome do Experimento", placeholder="Ex: Fungicida Soja 2024")
        
        col1, col2 = st.columns(2)
        n_trats = col1.number_input("Quantidade de Tratamentos", min_value=1, value=4)
        n_reps = col2.number_input("Quantidade de Repetições", min_value=1, value=4)
        
        st.write("---")
        st.subheader("Definição dos Produtos/Doses")
        
        # Criar campos dinâmicos para descrição de cada tratamento
        lista_descricoes = []
        for i in range(int(n_trats)):
            desc = st.text_input(f"Tratamento {i+1} (Produtos/Doses)", key=f"t{i}")
            lista_descricoes.append(desc)
            
        if st.button("Gerar Estrutura do Experimento"):
            novas_linhas = []
            for t_idx in range(int(n_trats)):
                for r_idx in range(int(n_reps)):
                    novas_linhas.append({
                        'Experimento': nome_exp,
                        'Tratamento': t_idx + 1,
                        'Descricao_Trat': lista_descricoes[t_idx],
                        'Repeticao': r_idx + 1,
                        'Variavel': 'N/A',
                        'Valor': 0.0,
                        'Data': datetime.now().strftime("%d/%m/%Y")
                    })
            
            df_novo = pd.concat([df_base, pd.DataFrame(novas_linhas)], ignore_index=True)
            salvar_dado(df_novo)
            st.success(f"Experimento '{nome_exp}' gerado com {n_trats * n_reps} unidades experimentais!")

# --- 2. COLETA DE CAMPO ---
elif menu == "2. Coleta de Campo":
    st.header("📝 Coleta por Repetição")
    
    if not df_base.empty:
        exp_selecionado = st.selectbox("Se
