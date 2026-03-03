import requests
import re

class IboManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Origin": "https://iboproapp.com",
            "Referer": "https://iboproapp.com/manage-playlists/login/"
        })
        self.base_url = "https://iboproapp.com"
        self.dns_base = "http://galaxy.blcplay1.com"

    def ativar_dispositivo(self, mac, key, user, password):
        # 1. Primeiro acessa a página para validar a sessão
        login_url = f"{self.base_url}/manage-playlists/login/"
        self.session.get(login_url)

        # 2. Define o nome com base em quantas listas já existem (ou fixo como sugerido)
        # Vamos usar um nome padrão que você pode numerar manualmente no painel se quiser
        nome_playlist = "ImperiumTv Server 1"
        
        # 3. Monta a URL do Galaxy
        playlist_url = f"{self.dns_base}/get.php?username={user}&password={password}&type=m3u_plus&output=mpegts"
        
        # 4. PIN de 5 dígitos (conforme solicitado)
        pin_5 = "12345"

        payload = {
            'mac_address': mac,
            'device_key': key,
            'playlist_name': nome_playlist,
            'playlist_url': playlist_url,
            'protect_pin': '1',
            'pin': pin_5,
            'confirm_pin': pin_5,
            'login_button': 'Login'
        }

        try:
            # Envia o POST simulando o botão "SUBMIT" do print
            response = self.session.post(login_url, data=payload, timeout=20)
            
            # Se o MAC estiver correto, o site redireciona para a lista
            if response.status_code == 200:
                return "Sucesso"
            return f"Erro do Servidor: {response.status_code}"
        except Exception as e:
            return f"Erro de Conexão: {str(e)}"

    def excluir_playlist(self, mac, key):
        url_delete = f"{self.base_url}/manage-playlists/delete-playlist/"
        payload = {'mac_address': mac, 'device_key': key}
        self.session.post(url_delete, data=payload, timeout=10)
