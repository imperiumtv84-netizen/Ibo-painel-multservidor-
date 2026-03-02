import requests
from bs4 import BeautifulSoup
import io

class IboManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        })
        self.base_url = "https://iboplayer.com"

    def iniciar_sessao(self):
        """Acessa a página de login para gerar o cookie e aceitar termos."""
        url = f"{self.base_url}/device/login"
        response = self.session.get(url)
        
        # Simula aceitação dos termos (Legal Terms)
        # É crucial enviar 'agree=1' para o IBO validar a sessão
        payload = {'agree': '1'}
        self.session.post(url, data=payload)
        
        return response.text

    def obter_captcha(self):
        """Captura a imagem do captcha atual."""
        self.iniciar_sessao()
        
        # Busca a URL do captcha no HTML
        url_captcha = f"{self.base_url}/captcha/image"
        response = self.session.get(url_captcha)
        
        if response.status_code == 200:
            return response.content # Retorna a imagem em bytes
        return None

    def ativar_dispositivo(self, mac, key, user, password, captcha_code, server_url):
        """Envia os dados de ativação."""
        url_post = f"{self.base_url}/device/login"
        
        payload = {
            'mac': mac,
            'key': key,
            'url': server_url,
            'username': user,
            'password': password,
            'captcha': captcha_code,
            'agree': '1' # Reafirma a aceitação dos termos
        }
        
        response = self.session.post(url_post, data=payload)
        return response.text
