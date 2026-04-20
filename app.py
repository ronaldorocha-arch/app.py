import streamlit as st
import pandas as pd
import random
from gtts import gTTS
import io
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Curso de Inglês IA", layout="wide")

# --- BANCO DE DADOS DE PERGUNTAS ---
PERGUNTAS = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "What are your salary expectations?",
    "How do you handle stress and pressure?",
    "What is your greatest professional achievement?",
    "Why are you leaving your current job?",
    "Where do you see yourself in five years?",
    "Do you prefer working alone or in a team?"
]

# --- CARREGAR VOCABULÁRIO ---
@st.cache_data
def load_words():
    try:
        return pd.read_csv('palavras.csv')
    except:
        return pd.DataFrame({"word": ["Ready"], "translation": ["Pronto"], "sentence": ["Are you ready?"]})

df_words = load_words()

# --- MEMÓRIA DO APP ---
if 'pontos_ronaldo' not in st.session_state: st.session_state.pontos_ronaldo = 0
if 'pontos_amigo' not in st.session_state: st.session_state.pontos_amigo = 0
if 'word_idx' not in st.session_state: st.session_state.word_idx = 0
if 'perg_idx' not in st.session_state: st.session_state.perg_idx = 0

# --- LOGIN ---
user = st.sidebar.selectbox("👤 Usuário", ["Ronaldo", "Amigo"])
pontos_atuais = st.session_state.pontos_ronaldo if user == "Ronaldo" else st.session_state.pontos_amigo
st.sidebar.metric("🏆 Seus Pontos", pontos_atuais)

def play(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp)

# --- INTERFACE ---
st.title("🇬🇧 English Mastery Course")

tab1, tab2, tab3 = st.tabs(["🎯 Vocabulário", "🎤 Entrevista", "📊 Ranking"])

with tab1:
    word = df_words.iloc[st.session_state.word_idx]
    st.header(f"Word: {word['word']}")
    if st.button("👁️ Mostrar Tradução"):
        st.success(f"Tradução: {word['translation']}")
        st.info(f"Exemplo: {word['sentence']}")
        play(word['sentence'])
    
    if st.button("Próxima Palavra ➡️"):
        st.session_state.word_idx = random.randint(0, len(df_words)-1)
        if user == "Ronaldo": st.session_state.pontos_ronaldo += 5
        else: st.session_state.pontos_amigo += 5
        st.rerun()

with tab2:
    perg = PERGUNTAS[st.session_state.perg_idx]
    st.subheader("Treino de Entrevista")
    st.warning(f"IA Pergunta: {perg}")
    if st.button("🔊 Ouvir Pergunta"): play(perg)
    
    audio = mic_recorder(start_prompt="🎤 Gravar Resposta", stop_prompt="🛑 Parar", key='entrevista')
    if audio:
        st.audio(audio['bytes'])
        st.success("Áudio gravado! Pratique a pronúncia ouvindo sua gravação.")

    if st.button("Trocar Pergunta 🔄"):
        st.session_state.perg_idx = (st.session_state.perg_idx + 1) % len(PERGUNTAS)
        if user == "Ronaldo": st.session_state.pontos_ronaldo += 10
        else: st.session_state.pontos_amigo += 10
        st.rerun()

with tab3:
    st.header("Placar do Desafio")
    data = {"Jogador": ["Ronaldo", "Amigo"], "Pontos": [st.session_state.pontos_ronaldo, st.session_state.pontos_amigo]}
    st.table(pd.DataFrame(data))
