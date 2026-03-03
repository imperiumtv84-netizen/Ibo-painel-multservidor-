import streamlit as st
from ibo_manager import IboManager

# Configuração da página
st.set_page_config(page_title="Painel IBO Pro", page_icon="🚀")
st.title("🚀 Painel de Ativação IBO Pro")
st.subheader("Ativação Direta - Sem Captcha")

# Inicializa o gerenciador
if 'manager' not in st.session_state:
    st.session_state.manager = IboManager()

# --- Formulário de Entrada ---
with st.form("form_ativacao"):
    col1, col2 = st.columns(2)
    with col1:
        mac = st.text_input("MAC Address", placeholder="00:1A:79:...")
        key = st.text_input("Device Key", type="password")
    with col2:
        server_url = st.text_input("URL do Servidor (DNS)", placeholder="http://exemplo.com:8080")
        user = st.text_input("Usuário IPTV")
        password = st.text_input("Senha IPTV", type="password")

    st.write("---")
    submit = st.form_submit_button("🚀 Ativar Playlist Agora")

# --- Processamento ---
if submit:
    if not mac or not key or not user or not password:
        st.warning("⚠️ Por favor, preencha todos os campos.")
    else:
        with st.spinner("Conectando ao IBO Pro..."):
            resultado = st.session_state.manager.ativar_dispositivo(
                mac, key, user, password, "", server_url
            )
            
            # Verificação de sucesso simples baseada no retorno do site
            if "success" in resultado.lower() or "added" in resultado.lower() or "successfully" in resultado.lower():
                st.success("✅ Playlist enviada com sucesso!")
            else:
                st.info("Processo concluído. Verifique o aplicativo.")
                with st.expander("Ver detalhes da resposta"):
                    st.code(resultado)
