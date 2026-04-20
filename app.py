import streamlit as st
import pandas as pd
import random
from gtts import gTTS
import io
from streamlit_mic_recorder import mic_recorder

# Configuração
st.set_page_config(page_title="English Mastery IA", layout="wide")

# Função para carregar palavras
@st.cache_data
def load_words():
    try:
        return pd.read_csv('palavras.csv')
    except:
        return pd.DataFrame({"word": ["Hello"], "translation": ["Olá"], "sentence": ["Hello, how are you?"]})

df_words = load_words()

# Inicializar Memória do Site (Session State)
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "Ronaldo": {"pontos": 0, "streak": 1},
        "Amigo": {"pontos": 0, "streak": 1}
    }
if 'word_index' not in st.session_state:
    st.session_state.word_index = random.randint(0, len(df_words)-1)

# Barra Lateral
st.sidebar.title("👤 Área do Aluno")
user = st.sidebar.selectbox("Quem está logado?", ["Ronaldo", "Amigo"])
st.sidebar.metric("🏆 Pontos", st.session_state.usuarios[user]['pontos'])

# Função de Voz da IA
def play_audio(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp, format='audio/mp3')

# ABAS
tab1, tab2, tab3 = st.tabs(["🗂️ Vocabulário (Anki)", "🎙️ Entrevista de Emprego", "🏆 Ranking"])

with tab1:
    st.header("O Homem do Vocabulário")
    atual = df_words.iloc[st.session_state.word_index]
    
    st.markdown(f"### Word: **{atual['word']}**")
    
    if st.button("Mostrar Tradução"):
        st.info(f"Tradução: {atual['translation']}")
        st.write(f"Exemplo: {atual['sentence']}")
        play_audio(atual['sentence'])

    st.write("---")
    col1, col2, col3 = st.columns(3)
    if col1.button("🟢 Fácil"):
        st.session_state.usuarios[user]['pontos'] += 5
        st.session_state.word_index = random.randint(0, len(df_words)-1)
        st.rerun()
    if col2.button("🟡 Médio"):
        st.session_state.usuarios[user]['pontos'] += 2
        st.session_state.word_index = random.randint(0, len(df_words)-1)
        st.rerun()
    if col3.button("🔴 Difícil"):
        st.session_state.word_index = random.randint(0, len(df_words)-1)
        st.rerun()

with tab2:
    st.header("Simulador de Entrevista Real")
    pergunta_ia = "Tell me about your professional background and goals."
    st.warning(f"IA: {pergunta_ia}")
    
    if st.button("🔊 Ouvir Pergunta"):
        play_audio(pergunta_ia)
    
    st.write("Clique no microfone abaixo e fale sua resposta:")
    # O BOTÃO DE MICROFONE REAL:
    audio = mic_recorder(start_prompt="🎤 Começar a Gravar", stop_prompt="🛑 Parar", key='recorder')
    
    if audio:
        st.audio(audio['bytes'])
        st.success("Áudio enviado! (A análise de texto requer chave de API, mas você já ganhou +10 pontos por praticar!)")
        st.session_state.usuarios[user]['pontos'] += 10

with tab3:
    st.header("Placar de Líderes")
    ranking = pd.DataFrame(st.session_state.usuarios).T
    st.table(ranking)
