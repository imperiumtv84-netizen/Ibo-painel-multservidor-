import streamlit as st
from ibo_manager import IboManager

st.set_page_config(page_title="Painel ImperiumTV", page_icon="📺")
st.title("📺 Painel ImperiumTV - IBO Pro")

if 'manager' not in st.session_state:
    st.session_state.manager = IboManager()

aba1, aba2 = st.tabs(["🚀 Ativação", "🗑️ Exclusão"])

with aba1:
    with st.form("form_ativacao"):
        col1, col2 = st.columns(2)
        with col1:
            mac = st.text_input("MAC Address")
            key = st.text_input("Device Key", type="password")
            server_num = st.selectbox("Selecione o Servidor", ["Server 1", "Server 2", "Server 3"])
        with col2:
            user = st.text_input("Usuário IPTV")
            password = st.text_input("Senha IPTV", type="password")
        
        submit = st.form_submit_button("🚀 Enviar para o IBO")

    if submit:
        with st.spinner("Conectando ao IBO Pro..."):
            # Passamos o número do servidor para o manager se desejar customizar
            res = st.session_state.manager.ativar_dispositivo(mac, key, user, password)
            if res == "Sucesso":
                st.success(f"✅ Enviado! Verifique a lista no site.")
            else:
                st.error(f"❌ Falha: {res}")
