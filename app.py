import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Meu Inglês com IA", layout="centered")

st.title("🚀 My English Mastery App")

# Simulando uma base de dados das 3000 palavras
# No futuro, isso pode vir de um arquivo Excel ou CSV
words_db = [
    {"word": "The", "translation": "O/A", "sentence": "The book is on the table."},
    {"word": "Management", "translation": "Gerenciamento", "sentence": "I have experience in project management."},
    {"word": "Challenge", "translation": "Desafio", "sentence": "I am looking for a new challenge."},
]

if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(words_db)

word = st.session_state.current_word

# Card de Estudo
st.subheader("Vocabulary Training")
with st.container():
    st.markdown(f"### Word: **{word['word']}**")
    
    if st.button("Show Meaning & Sentence"):
        st.info(f"**Tradução:** {word['translation']}")
        st.write(f"*Example:* {word['sentence']}")
    
    st.write("---")
    st.write("Como foi essa palavra para você?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Fácil"):
            st.success("Boa! Vamos demorar a mostrar essa de novo.")
            st.session_state.current_word = random.choice(words_db)
            # st.experimental_rerun() # Descomentar no app real
            
    with col2:
        if st.button("🟡 Médio"):
            st.warning("Ok, anotado. Revisão em breve.")
            st.session_state.current_word = random.choice(words_db)
            
    with col3:
        if st.button("🔴 Difícil"):
            st.error("Sem problemas! Vamos praticar mais vezes.")
            st.session_state.current_word = random.choice(words_db)

# Espaço para a IA (Placeholder por enquanto)
st.sidebar.title("Configurações")
if st.sidebar.button("Falar com IA (Beta)"):
    st.sidebar.write("Função de áudio será integrada aqui!")
