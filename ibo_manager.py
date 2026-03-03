import requests

class IboManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://iboproapp.com/manage-playlists/login/"
        })
        self.base_url = "https://iboproapp.com"
        # Substitua SEU_DNS_AQUI pelo DNS real que você quer esconder
        self.dns_fixo = "http://SEU_DNS_AQUI:8080" 

    def ativar_dispositivo(self, mac, key, user, password):
        url_post = f"{self.base_url}/manage-playlists/login/"
        
        # PIN Fixo solicitado: 1122334455
        pin_fixo = "1122334455"
        
        payload = {
            'mac_address': mac,
            'device_key': key,
            'username': user,
            'password': password,
            'xc_url': self.dns_fixo,
            'protect_pin': '1',        # Marca a caixa "Protect this playlist"
            'pin': pin_fixo,           # Campo PIN
            'confirm_pin': pin_fixo,   # Campo Confirm PIN
            'login_button': 'Login'
        }
        
        try:
            # Envia a requisição para o servidor
            r = self.session.post(url_post, data=payload, timeout=15)
            return r.text
        except Exception as e:
            return f"Erro: {str(e)}"

    def excluir_playlist(self, mac, key):
        """ Função para deletar playlist em massa """
        url_delete = f"{self.base_url}/manage-playlists/delete-playlist/"
        payload = {'mac_address': mac, 'device_key': key}
        try:
            self.session.post(url_delete, data=payload, timeout=10)
        except:
            pass
