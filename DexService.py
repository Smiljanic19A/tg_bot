import requests

class DexService:

    def __init__(self):
        self.latest_url = "https://api.dexscreener.com/token-profiles/latest/v1"
        pass

    def get_latest_token_profiles(self):
        response = requests.get(self.latest_url)
        return response.json()
