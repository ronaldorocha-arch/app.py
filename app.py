import streamlit as st
import pandas as pd
import random
from gtts import gTTS
import io
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="English Mastery IA", layout="wide")

# Lista de Perguntas de Entrevista
PERGUNTAS = [
    "Tell me about your professional background.",
    "What are your greatest professional strengths?",
    "Why do you want to work for this company?",
    "Where do you see yourself in five years?",
    "How do you handle pressure at work?"
]

@st.cache_data
def load_words():
    try:
        return pd.read_csv('palavras.csv')
    except:
        return pd.DataFrame({"word": ["Ready?"], "translation": ["Pronto?"], "sentence": ["Are you ready to study?"]})

df_words = load_words()

# Inicializar Memória
if 'pontos' not in st.session_state: st.session_state.pontos = 0
if 'word_idx' not in st.session_state: st.session_state.word_idx = 0
if 'pergunta_idx' not in st.session_state: st.session_state.pergunta_idx = 0

def play_audio(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp, format='audio/mp3')

st.sidebar.title("🚀 Status")
st.sidebar.metric("Seus Pontos", st.session_state.pontos)

tab1, tab2, tab3 = st.tabs(["🗂️ Vocabulário", "🎙️ Entrevista IA", "🏆 Ranking"])

with tab1:
    atual = df_words.iloc[st.session_state.word_idx]
    st.header(f"Palavra: {atual['word']}")
    if st.button("Ver Resposta"):
        st.success(f"Tradução: {atual['translation']}")
        st.write(f"Exemplo: {atual['sentence']}")
        play_audio(atual['sentence'])
    
    if st.button("Próxima Palavra ➡️"):
        st.session_state.word_idx = random.randint(0, len(df_words)-1)
        st.session_state.pontos += 5
        st.rerun()

with tab2:
    pergunta_atual = PERGUNTAS[st.session_state.pergunta_idx]
    st.subheader("Simulador de Voz")
    st.info(f"IA Pergunta: {pergunta_atual}")
    
    if st.button("🔊 Ouvir Pergunta"):
        play_audio(pergunta_atual)
    
    audio = mic_recorder(start_prompt="🎤 Falar Resposta", stop_prompt="🛑 Parar", key='entrevista')
    
    if audio:
        st.audio(audio['bytes'])
        st.success("Resposta enviada! Muito bem.")
        if st.button("Próxima Pergunta da Entrevista"):
            st.session_state.pergunta_idx = (st.session_state.pergunta_idx + 1) % len(PERGUNTAS)
            st.session_state.pontos += 10
            st.rerun()

with tab3:
    st.write("Em breve: Ranking persistente com seu amigo!")
