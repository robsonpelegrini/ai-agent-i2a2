import streamlit as st
from main import run_nf_assistant

st.set_page_config(page_title="NF Assistant Chat", layout="wide")

# --- Inicialização do estado da sessão ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou seu assistente fiscal. Pergunte algo sobre as notas fiscais do arquivo `202401_NFs_Cabecalho.csv` 📄"}
    ]

# --- Título da página ---
st.title("🧾 NF Assistant - Chat sobre Notas Fiscais")

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
        with st.spinner("⏳ Analisando suas notas fiscais..."):
            try:
                response = run_nf_assistant(user_prompt)
                ai_reply = response.raw
            except Exception as e:
                ai_reply = f"⚠️ Ocorreu um erro ao processar: {e}"
        st.code(ai_reply)

    # Salva a resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
