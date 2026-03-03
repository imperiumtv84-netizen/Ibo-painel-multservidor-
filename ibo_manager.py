import requests

class IboManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://iboproapp.com/manage-playlists/login/"
        })
        self.base_url = "https://iboproapp.com"
        # Seu DNS fixo
        self.dns_base = "http://galaxy.blcplay1.com" 

    def ativar_dispositivo(self, mac, key, user, password):
        url_post = f"{self.base_url}/manage-playlists/login/"
        
        # PIN de 5 dígitos solicitado
        pin_5_digitos = "12345"
        
        # MONTAGEM DA URL DINÂMICA (Padrão solicitado)
        # Ex: http://galaxy.blcplay1.com/get.php?username=USER&password=PASS&type=m3u_plus&output=mpegts
        playlist_url = f"{self.dns_base}/get.php?username={user}&password={password}&type=m3u_plus&output=mpegts"
        
        payload = {
            'mac_address': mac,
            'device_key': key,
            'playlist_name': 'ImperiumTV', # Nome que aparecerá no IBO
            'playlist_url': playlist_url,  # URL montada automaticamente
            'protect_pin': '1',
            'pin': pin_5_digitos,
            'confirm_pin': pin_5_digitos,
            'login_button': 'Login'
        }
        
        try:
            r = self.session.post(url_post, data=payload, timeout=15)
            return r.text
        except Exception as e:
            return f"Erro: {str(e)}"

    def excluir_playlist(self, mac, key):
        url_delete = f"{self.base_url}/manage-playlists/delete-playlist/"
        payload = {'mac_address': mac, 'device_key': key}
        try:
            self.session.post(url_delete, data=payload, timeout=10)
        except:
            pass
