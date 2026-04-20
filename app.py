import streamlit as st
import pandas as pd
import random
from gtts import gTTS
import io

# Configurações iniciais
st.set_page_config(page_title="English Duolingo IA", layout="wide")

# Simulação de Banco de Dados (Em um app real usaríamos um DB de verdade)
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "Ronaldo": {"pontos": 120, "streak": 5, "last_day": "2023-10-26"},
        "Amigo": {"pontos": 95, "streak": 3, "last_day": "2023-10-25"}
    }

# --- FUNÇÕES DE ÁUDIO ---
def falar(texto):
    tts = gTTS(text=texto, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

# --- LOGIN ---
st.sidebar.title("👤 Login")
user = st.sidebar.selectbox("Quem está estudando?", ["Ronaldo", "Amigo"])
st.sidebar.write(f"🔥 Streak: {st.session_state.usuarios[user]['streak']} dias")
st.sidebar.write(f"🏆 Pontos: {st.session_state.usuarios[user]['pontos']}")

st.title(f"Welcome back, {user}! 🚀")

# --- ABAS ---
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Desafio/Ranking", "🎧 Listening Lab", "🎙️ Job Interview", "🗂️ Vocabulário"])

with tab1:
    st.header("Ranking dos Campeões")
    df_ranking = pd.DataFrame(st.session_state.usuarios).T[['pontos', 'streak']]
    st.table(df_ranking)
    st.progress(st.session_state.usuarios[user]['pontos'] / 200)
    st.write("Meta da semana: 200 pontos")

with tab2:
    st.header("O que a IA disse?")
    texto_listening = "I have been working as a software engineer for five years and I am looking for a new challenge in a global company."
    
    if st.button("🔊 Ouvir Áudio"):
        audio_fp = falar(texto_listening)
        st.audio(audio_fp, format='audio/mp3')
    
    escolha = st.radio("Sobre o que foi o assunto?", ["Culinária", "Carreira Profissional", "Viagem", "Saúde"])
    if st.button("Confirmar Resposta"):
        if escolha == "Carreira Profissional":
            st.success("Correct! +10 points")
            st.session_state.usuarios[user]['pontos'] += 10
        else:
            st.error("Wrong answer. Try again!")

with tab3:
    st.header("Simulador de Entrevista")
    pergunta = "What are your professional strengths?"
    st.info(f"IA asks: {pergunta}")
    
    if st.button("🔊 Ouvir Pergunta"):
        st.audio(falar(pergunta), format='audio/mp3')
        
    resposta = st.text_area("Sua resposta (Dite ou digite):")
    if st.button("Analisar Resposta"):
        if "experience" in resposta.lower() or "skills" in resposta.lower():
            st.success("Boa! Você usou palavras-chave importantes. +5 pontos")
            st.session_state.usuarios[user]['pontos'] += 5
        else:
            st.warning("Tente incluir suas habilidades e experiências na resposta.")

with tab4:
    st.header("Repetição Espaçada")
    st.write("Sistema de 3000 palavras em construção...")
