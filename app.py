import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração de persistência
DATA_FILE = "dados_estacao_v2.csv"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except:
            return pd.DataFrame(columns=['Experimento', 'Tratamento', 'Descricao_Trat', 'Repeticao', 'Variavel', 'Valor', 'Data'])
    return pd.DataFrame(columns=['Experimento', 'Tratamento', 'Descricao_Trat', 'Repeticao', 'Variavel', 'Valor', 'Data'])

def salvar_dado(df):
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="BioField Pro", layout="wide")
df_base = carregar_dados()

st.sidebar.title("🌱 Estação Experimental")
menu = st.sidebar.radio("Navegação", ["1. Configurar Experimento", "2. Coleta de Campo", "3. Exportar Relatório"])

# --- 1. CONFIGURAR EXPERIMENTO ---
if menu == "1. Configurar Experimento":
    st.header("🔬 Novo Delineamento")
    
    with st.expander("Cadastrar novo experimento", expanded=True):
        nome_exp = st.text_input("Nome do Experimento")
        col1, col2 = st.columns(2)
        n_trats = col1.number_input("Quantidade de Tratamentos", min_value=1, value=4)
        n_reps = col2.number_input("Quantidade de Repetições", min_value=1, value=4)
        
        st.subheader("Definição dos Tratamentos")
        lista_descricoes = []
        for i in range(int(n_trats)):
            desc = st.text_input(f"Tratamento {i+1} (Produtos/Doses)", key=f"t{i}")
            lista_descricoes.append(desc)
            
        if st.button("Gerar Estrutura"):
            novas_linhas = []
            for t_idx in range(int(n_trats)):
                for r_idx in range(int(n_reps)):
                    novas_linhas.append({
                        'Experimento': nome_exp,
                        'Tratamento': t_idx + 1,
                        'Descricao_Trat': lista_descricoes[t_idx],
                        'Repeticao': r_idx + 1,
                        'Variavel': 'Inicial',
                        'Valor': 0.0,
                        'Data': datetime.now().strftime("%d/%m/%Y")
                    })
            df_final = pd.concat([df_base, pd.DataFrame(novas_linhas)], ignore_index=True)
            salvar_dado(df_final)
            st.success("Experimento Gerado!")

# --- 2. COLETA DE CAMPO ---
elif menu == "2. Coleta de Campo":
    st.header("📝 Coleta por Repetição")
    if not df_base.empty:
        exps = df_base['Experimento'].unique()
        exp_sel = st.selectbox("Selecione o Experimento", exps)
        df_exp = df_base[df_base['Experimento'] == exp_sel]
        
        col_t, col_r = st.columns(2)
        t_sel = col_t.selectbox("Tratamento", sorted(df_exp['Tratamento'].unique()))
        
        desc_atual = df_exp[df_exp['Tratamento'] == t_sel]['Descricao_Trat'].iloc[0]
        st.info(f"**Composição:** {desc_atual}")
        
        r_sel = col_r.selectbox("Repetição", sorted(df_exp[df_exp['Tratamento'] == t_sel]['Repeticao'].unique()))
        
        st.write("---")
        v_nome = st.text_input("Variável (ex: Altura, Stand)")
        v_valor = st.number_input("Valor", format="%.4f")
        
        if st.button("Salvar Leitura"):
            nova_leitura = pd.DataFrame([{
                'Experimento': exp_sel, 'Tratamento': t_sel, 'Descricao_Trat': desc_atual,
                'Repeticao': r_sel, 'Variavel': v_nome, 'Valor': v_valor,
                'Data': datetime.now().strftime("%d/%m/%Y %H:%M")
            }])
            salvar_dado(pd.concat([df_base, nova_leitura], ignore_index=True))
            st.toast("Registrado!")
    else:
        st.warning("Cadastre um experimento primeiro.")

# --- 3. EXPORTAR RELATÓRIO ---
elif menu == "3. Exportar Relatório":
    st.header("📊 Banco de Dados")
    st.dataframe(df_base)
    csv = df_base.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar Excel", csv, "dados.csv", "text/csv")
