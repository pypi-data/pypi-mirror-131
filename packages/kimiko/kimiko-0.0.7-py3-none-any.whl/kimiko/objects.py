import requests
from urllib.parse import urlencode

class Objects:
    base_url = 'https://objects.kimiko.io/v1'

    def __init__(self, account_id, api_key):
        self.account_id = account_id
        self.api_key = api_key
        self.url_auth = f'account_id={self.account_id}&api_key={self.api_key}'


    @classmethod
    def client(cls, account_id, api_key):
        return cls(account_id, api_key)
    

    def objects(self):
        r = requests.get(f'{Objects.base_url}?{self.url_auth}')
        if r.ok:
            return r.json().get('data')
        else:
            return []

    def create_object(self, object_key: str, name: str, fields: dict = None, unique_fields: list = None):
        data = {k:v for k,v in ({'object_key': object_key, 'name': name, 'fields': fields, 'unique_fields': unique_fields}).items()}
        r = requests.post(f'{Objects.base_url}?{self.url_auth}', json=data)
        return r.json()

    def update_object(self, object_key, **kwargs):
        r = requests.put(f'{Objects.base_url}/{object_key}?{self.url_auth}', json={k:v for k,v in kwargs.items()})
        return r.json()

    def delete_object(self, object_key):
        r = requests.delete(f'{Objects.base_url}/{object_key}?{self.url_auth}')
        return r.json()


    def records(self, object_key, limit_=None, **kwargs):
        r = requests.get(f'{Objects.base_url}/{object_key}/records?{self.url_auth}')
        if r.ok:
            data = r.json().get('data')
            for k,v in kwargs.items():
                data = list(filter(lambda x: x.get(k) == v, data))
            return data
        else:
            print(r.json())
            return []

    def create_record(self, object_key, **kwargs):
        r = requests.post(f'{Objects.base_url}/{object_key}/records?{self.url_auth}', json={k:v for k,v in kwargs.items()})
        return r.json()


    def update_record(self, object_key, record_id, **kwargs):
        r = requests.put(f'{Objects.base_url}/{object_key}/records/{record_id}?{self.url_auth}', json={k:v for k,v in kwargs.items()})
        return r.json()

    def delete_record(self, object_key, record_id):
        r = requests.delete(f'{Objects.base_url}/{object_key}/records/{record_id}?{self.url_auth}')
        return r.json()

    def search_records(self, object_key, **kwargs):
        url = f'{Objects.base_url}/{object_key}/records/search?{self.url_auth}'
        url = url + f'&{urlencode(kwargs)}' if kwargs else url
        r = requests.get(url)
        return r.json()