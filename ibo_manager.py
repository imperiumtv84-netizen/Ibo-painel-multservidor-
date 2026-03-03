import requests

class IboManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://iboproapp.com/manage-playlists/login/"
        })
        # Nova URL Base
        self.base_url = "https://iboproapp.com"

    def obter_captcha(self):
        """Retorna None já que o IBO Pro não possui captcha."""
        return None

    def ativar_dispositivo(self, mac, key, user, password, captcha_code, server_url):
        """Envia os dados para o novo endpoint do IBO Pro."""
        # O endpoint de login pode variar, geralmente é o mesmo da página de login
        url_post = f"{self.base_url}/manage-playlists/login/"
        
        payload = {
            'mac_address': mac, # Verifique se no site é 'mac' ou 'mac_address'
            'device_key': key,
            'username': user,
            'password': password,
            'xc_url': server_url,
            'login_button': 'Login'
        }
        
        response = self.session.post(url_post, data=payload)
        return response.text
