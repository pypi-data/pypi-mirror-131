import time

import requests

from helpers import hash_by_sha256, hash_by_md5


class FreekassaApi:
    API_BASE_URL = 'https://api.freekassa.ru/v1/{method}'
    INVOICE_BASE_URL = 'https://pay.freekassa.ru/?{query}'

    def __init__(self, shop_id: int, secret1: str, secret2: str, api_key: str):
        self.session = requests.Session()

        self.shop_id = shop_id
        self.secret1 = secret1
        self.secret2 = secret2
        self.api_key = api_key

    def generate_api_signature(self, json: dict) -> str:
        sorted_values = []

        for key in sorted(json.keys()):
            sorted_values.append(str(json[key]))

        return hash_by_sha256(self.api_key, '|'.join(sorted_values))

    def generate_payment_form_signature(self, amount: int, order_id: str, currency='RUB') -> str:
        return hash_by_md5(f'{self.shop_id}:{amount}:{self.secret1}:{currency}:{order_id}')

    def request(self, method: str, json: dict = None) -> dict:
        url = self.API_BASE_URL.format(method=method)

        json = json or {}
        json = {k: v for k, v in json.items() if v is not None}
        json = {**json, 'shopId': self.shop_id, 'nonce': time.time_ns()}
        json = {**json, 'signature': self.generate_api_signature(json)}

        resp = self.session.post(url, json=json)
        return resp.json()
