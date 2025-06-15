import streamlit as st
from main import run_nf_assistant
import os

st.set_page_config(page_title="NF Assistant Chat", layout="wide")

# Debug - mostrar porta
port = os.getenv('PORT', '8501')
st.sidebar.write(f"Porta Railway: {port}")

# --- Inicialização do estado da sessão ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou seu assistente fiscal. \n"
        "Pergunte algo sobre o arquivo de notas fiscais que você selecionou acima 📄. \n"
        "*** Serão exibidos tabelas com no maximo 20 linhas como resposta. ***"}
    ]

# --- Título da página ---
st.title("🧾 NF Assistant - Chat sobre Notas Fiscais")

# Lista arquivos na pasta 'data'
data_dir = os.path.join(os.path.dirname(__file__), "data")

# Verifica se a pasta existe
if not os.path.exists(data_dir):
    st.error(f"Pasta 'data' não encontrada: {data_dir}")
    st.stop()

# Lista apenas arquivos (não diretórios)
try:
    file_options = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    
    if not file_options:
        st.warning("Nenhum arquivo encontrado na pasta 'data'")
        st.stop()
        
except Exception as e:
    st.error(f"Erro ao listar arquivos: {e}")
    st.stop()

# Seleção do arquivo pelo usuário como lista de seleção
selected_file = st.radio("Primeiramente selecione o arquivo de notas fiscais sobre qual você ira fazer suas perguntas:", file_options)

# Guarda o nome do arquivo selecionado na sessão
st.session_state.selected_file = selected_file
print(f"Arquivo selecionado: {st.session_state.selected_file}")

# --- Exibir histórico de mensagens com st.code para o assistente ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.code(msg["content"])
        else:
            st.markdown(msg["content"])

# --- Entrada do usuário ---
user_prompt = st.chat_input("Digite sua pergunta sobre as notas fiscais...")

# --- Processamento da pergunta ---
if user_prompt:
    # Adiciona pergunta ao histórico
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        # Constrói o caminho completo do arquivo corretamente
        file_path = os.path.join(data_dir, selected_file)
        
        with st.spinner(f"⏳ Analisando os dados do arquivo {file_path}"):
            try:
                print(f"Caminho completo do arquivo: {file_path}")
                
                # Verifica se o arquivo existe antes de processar
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
                
                response = run_nf_assistant(user_prompt, file_path)
                ai_reply = response.raw
                
            except Exception as e:
                ai_reply = f"⚠️ Ocorreu um erro ao processar: {e}"
                
        st.code(ai_reply)

    # Salva a resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})