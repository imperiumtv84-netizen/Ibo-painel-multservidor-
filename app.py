import streamlit as st
from ibo_manager import IboManager

st.set_page_config(page_title="Painel ImperiumTV", page_icon="📺")
st.title("📺 Painel ImperiumTV - IBO Pro")

if 'manager' not in st.session_state:
    st.session_state.manager = IboManager()

aba1, aba2 = st.tabs(["🚀 Ativação Automática", "🗑️ Limpeza em Massa"])

with aba1:
    st.subheader("Configurar Dispositivo")
    st.info("🔒 Playlist protegida com PIN de 5 dígitos.")
    
    with st.form("form_ativacao"):
        c1, c2 = st.columns(2)
        with c1:
            mac = st.text_input("MAC Address", placeholder="00:1A:79:...")
            key = st.text_input("Device Key", type="password")
        with c2:
            user = st.text_input("Usuário IPTV")
            password = st.text_input("Senha IPTV", type="password")
        
        submit = st.form_submit_button("🚀 Enviar para o IBO")

    if submit:
        if not all([mac, key, user, password]):
            st.warning("Preencha todos os campos!")
        else:
            with st.spinner("Gerando playlist e enviando..."):
                res = st.session_state.manager.ativar_dispositivo(mac, key, user, password)
                st.success(f"✅ Playlist enviada para o MAC {mac}!")
                st.caption("A lista aparecerá no App como 'ImperiumTV'.")

with aba2:
    st.subheader("Excluir Listas")
    lista_excluir = st.text_area("Formato: MAC|KEY (uma por linha)", height=150)
    
    if st.button("🗑️ Iniciar Exclusão"):
        linhas = [l for l in lista_excluir.split('\n') if '|' in l]
        if linhas:
            progresso = st.progress(0)
            for i, linha in enumerate(linhas):
                m, k = linha.split('|')
                st.session_state.manager.excluir_playlist(m.strip(), k.strip())
                progresso.progress((i + 1) / len(linhas))
            st.success("🏁 Limpeza concluída!")
