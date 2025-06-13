import streamlit as st
from main import run_nf_assistant
import os

st.set_page_config(page_title="NF Assistant Chat", layout="wide")

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
file_options = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

# Seleção do arquivo pelo usuário como lista de seleção
selected_file = st.radio("Primeiramente selecione o arquivo de notas fiscais sobre qual você ira fazer suas perguntas:", file_options)

# Guarda o nome do arquivo selecionado na sessão
st.session_state.selected_file = selected_file
print(st.session_state.selected_file)


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
        with st.spinner(f"⏳ Analisando os dados do arquivo {data_dir}/{selected_file}" ):
            try:
                print(f"Arquivo selecionado: {data_dir}/{selected_file}")
                
                response = run_nf_assistant(user_prompt, f".{data_dir}/{selected_file}")
                ai_reply = response.raw
            except Exception as e:
                ai_reply = f"⚠️ Ocorreu um erro ao processar: {e}"
        st.code(ai_reply)

    # Salva a resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
