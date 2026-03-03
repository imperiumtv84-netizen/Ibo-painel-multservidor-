import streamlit as st
from ibo_manager import IboManager

# Configuração da página
st.set_page_config(page_title="Gestor IBO Pro", page_icon="🛡️")

# --- SISTEMA DE LOGIN ---
SENHA_MESTRE = "11223344"

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acesso Restrito")
    senha_input = st.text_input("Digite a senha do painel:", type="password")
    if st.button("Entrar"):
        if senha_input == SENHA_MESTRE:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# --- PAINEL AUTENTICADO ---
st.title("🛡️ Gestor IBO Pro")

if 'manager' not in st.session_state:
    st.session_state.manager = IboManager()

aba1, aba2 = st.tabs(["🚀 Ativação Direta", "🗑️ Exclusão em Massa"])

with aba1:
    st.subheader("Enviar Nova Playlist")
    with st.form("form_ativacao"):
        col1, col2 = st.columns(2)
        with col1:
            mac = st.text_input("MAC Address", placeholder="00:1A:79:...")
            key = st.text_input("Device Key", type="password")
        with col2:
            user = st.text_input("Usuário IPTV")
            password = st.text_input("Senha IPTV", type="password")
        
        st.info("ℹ️ O DNS está configurado automaticamente no sistema.")
        submit = st.form_submit_button("🚀 Ativar Agora")

    if submit:
        with st.spinner("Processando..."):
            res = st.session_state.manager.ativar_dispositivo(mac, key, user, password)
            if "success" in res.lower() or "added" in res.lower():
                st.success(f"✅ MAC {mac} ativado!")
            else:
                st.warning("Verifique se os dados estão corretos no App.")

with aba2:
    st.subheader("Limpar Playlists")
    st.write("Insira os MACs e Keys (um por linha) no formato: `MAC|KEY`")
    lista_excluir = st.text_area("Exemplo: 00:11:22|123456", height=150)
    
    if st.button("🗑️ Excluir Todas as Listadas"):
        linhas = lista_excluir.split('\n')
        progresso = st.progress(0)
        for i, linha in enumerate(linhas):
            if '|' in linha:
                m, k = linha.split('|')
                st.session_state.manager.excluir_playlist(m.strip(), k.strip())
            progresso.progress((i + 1) / len(linhas))
        st.success("🏁 Processo de exclusão em massa finalizado!")
