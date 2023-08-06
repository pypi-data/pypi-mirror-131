import requests
import zapy

class API():
    def __init__(self, url, api_key):
        self.api_key = api_key
        self.url = url[:-1] if url.endswith('/') else url
        self.HTTP = requests.Session()
        self.HTTP.headers.update(
            {'X-ZAP-API-Key': self.api_key}
        )

        {{ API_CLASSES }}

    def close(self):
        self.HTTP.close()
