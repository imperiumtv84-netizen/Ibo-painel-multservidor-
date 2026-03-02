import streamlit as st
from ibo_manager 
from PIL import Image
import io

# Configuração da página
st.set_page_config(page_title="Painel IBO", page_icon="📺")
st.title("📺 Painel de Ativação IBO Player")

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
        server_url = st.text_input("URL do Servidor (DNS)")
        user = st.text_input("Usuário IPTV")
        password = st.text_input("Senha IPTV", type="password")

    st.write("---")
    
    # Botão para tentar carregar o captcha
    if st.form_submit_button("Tentar Carregar Captcha"):
        st.rerun()

    # Busca e exibe o captcha
    captcha_bytes = st.session_state.manager.obter_captcha()
    
    if captcha_bytes:
        try:
            image = Image.open(io.BytesIO(captcha_bytes))
            st.image(image, caption="Digite o código acima")
        except Exception as e:
            st.error(f"Erro ao processar imagem. O servidor do IBO pode estar bloqueando: {e}")
    else:
        st.warning("Não foi possível carregar a imagem do captcha.")
    
    captcha_code = st.text_input("Código do Captcha")
    submit = st.form_submit_button("Ativar Dispositivo")

# --- Processamento ---
if submit:
    if not captcha_code:
        st.error("Por favor, digite o código do captcha.")
    else:
        with st.spinner("Enviando dados..."):
            resultado = st.session_state.manager.ativar_dispositivo(
                mac, key, user, password, captcha_code, server_url
            )
            
            # Analisa o retorno
            if "success" in resultado.lower() or "added" in resultado.lower():
                st.success("✅ Dispositivo ativado com sucesso!")
            else:
                st.error("❌ Falha na ativação. Verifique o captcha ou os dados.")
                st.code(resultado)
