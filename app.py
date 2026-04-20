import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="My English IA", page_icon="🇬🇧")

# Carregar as palavras do arquivo que você criou
@st.cache_data
def load_data():
    try:
        return pd.read_csv('palavras.csv')
    except:
        return pd.DataFrame({"word": ["Study"], "translation": ["Estudar"], "sentence": ["I love to study."]})

df = load_data()

st.title("🎓 English Mastery App")

aba1, aba2 = st.tabs(["🗂️ Vocabulário (Anki)", "🎙️ Entrevista com IA"])

with aba1:
    st.subheader("O Homem do Vocabulário")
    
    if 'index' not in st.session_state:
        st.session_state.index = 0

    word_data = df.iloc[st.session_state.index]

    st.markdown(f"## {word_data['word']}")
    
    if st.button("Ver Tradução e Exemplo"):
        st.info(f"**Tradução:** {word_data['translation']}")
        st.write(f"**Exemplo:** {word_data['sentence']}")

    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🟢 Fácil"):
            st.session_state.index = random.randint(0, len(df)-1)
            st.rerun()
    with col2:
        if st.button("🟡 Médio"):
            st.session_state.index = random.randint(0, len(df)-1)
            st.rerun()
    with col3:
        if st.button("🔴 Difícil"):
            st.session_state.index = random.randint(0, len(df)-1)
            st.rerun()

with aba2:
    st.subheader("Treino para Entrevista")
    st.write("A IA vai analisar sua resposta abaixo:")
    
    pergunta = "Tell me about yourself and your professional background."
    st.warning(f"Pergunta da IA: {pergunta}")
    
    resposta = st.text_area("Digite sua resposta em inglês aqui (ou use o microfone do teclado):")
    
    if st.button("Analisar minha fala"):
        if resposta:
            st.success("Analisando...")
            # Aqui no futuro conectaremos a chave da API para uma análise real profunda
            st.write("Dica da IA: Você usou bem os tempos verbais, mas tente usar palavras como 'achievements' para soar mais profissional.")
        else:
            st.error("Por favor, escreva algo para eu analisar.")
