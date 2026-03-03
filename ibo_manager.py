import requests

class IboManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://iboproapp.com/manage-playlists/login/"
        })
        self.base_url = "https://iboproapp.com"
        # O DNS fica escondido aqui no código:
        self.dns_fixo = "http://SEU_DNS_AQUI:8080" 

    def ativar_dispositivo(self, mac, key, user, password):
        url_post = f"{self.base_url}/manage-playlists/login/"
        payload = {
            'mac_address': mac,
            'device_key': key,
            'username': user,
            'password': password,
            'xc_url': self.dns_fixo, # Usa o DNS oculto
            'login_button': 'Login'
        }
        try:
            r = self.session.post(url_post, data=payload, timeout=15)
            return r.text
        except:
            return "erro"

    def excluir_playlist(self, mac, key):
        """ Função para deletar playlist (Simula o comando de delete do site) """
        url_delete = f"{self.base_url}/manage-playlists/delete-playlist/"
        payload = {'mac_address': mac, 'device_key': key}
        self.session.post(url_delete, data=payload)
