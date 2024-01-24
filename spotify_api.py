import requests
from urllib.parse import urlencode

class SpotifyAPI:
    access_token = None
    access_token_expires = None
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_credentials = f"{self.client_id}:{self.client_secret}"
        client_credentials_b64 = base64.b64encode(client_credentials.encode())
        return client_credentials_b64.decode()

    def get_token_headers(self):
        client_credentials_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_credentials_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        
        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        self.access_token = access_token
        self.access_token_expires = now + datetime.timedelta(seconds=expires_in)
        return True

    def _authenticated_request(self, url, data=None, headers=None):
        if not self.access_token or self.access_token_expires < datetime.datetime.now():
            self.perform_auth()
        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.access_token}"
        r = requests.get(url, data=data, headers=headers)
        return r.json()

    def get_user_data(self):
        return self._authenticated_request(f"https://api.spotify.com/v1/me")

    def get_user_playlists(self):
        return self._authenticated_request(f"https://api.spotify.com/v1/me/playlists")