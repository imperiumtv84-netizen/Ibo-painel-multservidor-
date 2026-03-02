import requests
from bs4 import BeautifulSoup
import io

class IboManager:
    def __init__(self):
        self.session = requests.Session()
        # MELHORIA: User-Agent mais robusto e aceitação de imagens
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://iboplayer.com/device/login"
        })
        self.base_url = "https://iboplayer.com"

    def iniciar_sessao(self):
        """Acessa a página de login para gerar o cookie e aceitar termos."""
        url = f"{self.base_url}/device/login"
        # Faz um GET inicial para pegar cookies
        self.session.get(url)
        
        # Simula aceitação dos termos (Legal Terms)
        payload = {'agree': '1'}
        self.session.post(url, data=payload)

    def obter_captcha(self):
        """Captura a imagem do captcha atual."""
        self.iniciar_sessao()
        
        url_captcha = f"{self.base_url}/captcha/image"
        # Faz a requisição da imagem
        response = self.session.get(url_captcha)
        
        # Verifica se recebemos uma imagem
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            return response.content
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
            'agree': '1'
        }
        
        response = self.session.post(url_post, data=payload)
        return response.text
