import requests


class YandexDiskAPI:
    def __init__(self, token):
        self.token = token
        self.url_ya_poligon = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.url_yad = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def create_folder(self, path):
        requests.put(f'{self.url_ya_poligon}?path={path}', headers=self.headers)

    def upload_photo(self, file_name, url, path):
        requests.post(self.url_yad, headers=self.headers, params={'url': url, 'path': path})