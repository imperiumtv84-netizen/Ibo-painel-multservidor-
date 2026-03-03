import streamlit as st
from ibo_manager import IboManager

st.set_page_config(page_title="Gestor IBO Pro", page_icon="🛡️")
st.title("🛡️ Gestor IBO Pro")

if 'manager' not in st.session_state:
    st.session_state.manager = IboManager()

aba1, aba2 = st.tabs(["🚀 Ativação com PIN", "🗑️ Exclusão em Massa"])

with aba1:
    st.subheader("Enviar Playlist Protegida")
    st.info("🔒 Todas as listas serão protegidas com o PIN: 1122334455")
    
    with st.form("form_ativacao"):
        col1, col2 = st.columns(2)
        with col1:
            mac = st.text_input("MAC Address", placeholder="00:1A:79:...")
            key = st.text_input("Device Key", type="password")
        with col2:
            user = st.text_input("Usuário IPTV")
            password = st.text_input("Senha IPTV", type="password")
        
        submit = st.form_submit_button("🚀 Ativar Agora")

    if submit:
        with st.spinner("Enviando para o IBO Pro..."):
            res = st.session_state.manager.ativar_dispositivo(mac, key, user, password)
            st.success(f"✅ Comando enviado para o MAC {mac}!")

with aba2:
    st.subheader("Limpar Playlists")
    st.write("Insira os dados no formato: `MAC|KEY` (um por linha)")
    lista_excluir = st.text_area("Exemplo:\n00:11:22:AA:BB:CC|123456", height=150)
    
    if st.button("🗑️ Excluir Todas"):
        linhas = [l for l in lista_excluir.split('\n') if '|' in l]
        if linhas:
            progresso = st.progress(0)
            for i, linha in enumerate(linhas):
                m, k = linha.split('|')
                st.session_state.manager.excluir_playlist(m.strip(), k.strip())
                progresso.progress((i + 1) / len(linhas))
            st.success("🏁 Limpeza concluída!")
        else:
            st.error("Formato inválido. Use MAC|KEY")
