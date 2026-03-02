import streamlit as st
from ibo_manager import IboManager
from PIL import Image
import io

# Configuração da página
st.set_page_config(page_title="Painel IBO", page_icon="📺")
st.title("📺 Painel de Ativação IBO Player")

# Inicializa o gerenciador na sessão do Streamlit
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

    # --- Captcha ---
    st.write("---")
    
    # Busca e exibe o captcha
    captcha_bytes = st.session_state.manager.obter_captcha()
    
    if captcha_bytes:
        try:
            image = Image.open(io.BytesIO(captcha_bytes))
            st.image(image, caption="Digite o código acima")
        except Exception as e:
            st.error(f"Erro ao processar imagem: {e}")
            # Mostra o conteúdo recebido para debug
            st.code(captcha_bytes[:100])
    else:
        st.warning("Não foi possível carregar a imagem do captcha.")

    if st.form_submit_button("Atualizar Captcha"):
        st.rerun()
    
    captcha_code = st.text_input("Código do Captcha")
    
    # Botão Final
    submit = st.form_submit_button("Ativar Dispositivo")

# --- Processamento ---
if submit:
    with st.spinner("Enviando dados..."):
        resultado = st.session_state.manager.ativar_dispositivo(
            mac, key, user, password, captcha_code, server_url
        )
        
        # Analisa o retorno (Precisa verificar se o IBO retornou sucesso)
        if "success" in resultado.lower() or "added" in resultado.lower():
            st.success("✅ Dispositivo ativado com sucesso!")
        else:
            st.error("❌ Falha na ativação. Verifique o captcha ou os dados.")
            st.code(resultado) # Mostra o retorno cru para debug
