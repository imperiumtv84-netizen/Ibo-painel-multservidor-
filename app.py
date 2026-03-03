import streamlit as st

st.set_page_config(page_title="ImperiumTV - Massa", page_icon="📺")
st.title("📺 Adição em Massa ImperiumTV")

# Configurações Fixas
DNS_BASE = "http://galaxy.blcplay1.com"
PIN_5 = "12345"

st.info("💡 Como o IBO bloqueia robôs, use esta ferramenta para gerar a lista de URLs prontas.")

# --- ABA DE ADIÇÃO EM MASSA ---
st.subheader("🚀 Gerador de Links em Lote")
st.write("Insira os dados no formato: `MAC|KEY|USER|PASS` (um por linha)")
lista_massa = st.text_area("Lista de Clientes", height=200, placeholder="00:11:22:33:44:55|654321|usuario123|senha123")

if st.button("🔗 Gerar Tudo"):
    if not lista_massa:
        st.error("Insira ao menos uma linha!")
    else:
        linhas = [l.strip() for l in lista_massa.split('\n') if '|' in l]
        
        st.write(f"### ✅ {len(linhas)} Links Gerados")
        
        # Criamos uma tabela para facilitar a cópia individual se necessário
        for linha in linhas:
            try:
                m, k, u, p = linha.split('|')
                link_final = f"{DNS_BASE}/get.php?username={u}&password={p}&type=m3u_plus&output=mpegts"
                
                with st.expander(f"MAC: {m}"):
                    st.code(f"URL: {link_final}\nPIN: {PIN_5}")
                    st.button(f"Copiar link de {m}", on_click=lambda l=link_final: st.write(f"Copiado: {l}"), key=m)
            except:
                st.warning(f"Linha inválida: {linha}")

# --- ABA DE EXCLUSÃO (TEXTO PURO) ---
st.divider()
st.subheader("🗑️ Formatação para Exclusão")
st.write("Use esta área para organizar seus MACs de limpeza.")
# Aqui mantemos apenas um bloco de notas para organização do usuário
