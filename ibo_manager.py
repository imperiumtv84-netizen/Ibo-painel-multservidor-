import requests
import time

class IboManager:
    def __init__(self):
        self.session = requests.Session()
        # Headers idênticos a um navegador real para tentar burlar a Cloudflare
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://iboproapp.com",
            "Referer": "https://iboproapp.com/manage-playlists/login/"
        })

    def ativar_dispositivo(self, mac, key, user, password, server_name="ImperiumTV"):
        url_post = "https://iboproapp.com/manage-playlists/login/"
        
        # O link que você já tem completo, montado com o user e password do formulário
        link_playlist = f"http://galaxy.blcplay1.com/get.php?username={user}&password={password}&type=m3u_plus&output=mpegts"
        
        payload = {
            'mac_address': mac,
            'device_key': key,
            'playlist_name': server_name,
            'playlist_url': link_playlist,
            'protect_pin': '1',
            'pin': '12345',
            'confirm_pin': '12345',
            'login_button': 'Login'
        }

        try:
            # Pequena pausa para não parecer um robô disparando
            time.sleep(2)
            response = self.session.post(url_post, data=payload, timeout=30)
            
            # Se a resposta contiver o MAC, geralmente significa que logou e mostrou a lista
            if mac.lower() in response.text.lower():
                return "Sucesso"
            else:
                return "Bloqueado pela Cloudflare ou Dados Incorretos"
        except Exception as e:
            return f"Erro: {str(e)}"

    def excluir_playlist(self, mac, key):
        url_delete = "https://iboproapp.com/manage-playlists/delete-playlist/"
        payload = {'mac_address': mac, 'device_key': key}
        self.session.post(url_delete, data=payload, timeout=10)
