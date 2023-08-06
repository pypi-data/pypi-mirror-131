from urllib.parse import urlencode

from . import models
from .api_base import FreekassaApi
from .constants import Currencies


class Merchant(FreekassaApi):

    def get_payment_form_url(self, amount: int, order_id: str, currency=Currencies.RUB, payment_method: int = None,
                             phone: str = None, email: str = None, lang: str = None) -> str:
        params = {
            'm': self.shop_id,
            'oa': amount,
            'currency': currency,
            'o': order_id,
            's': self.generate_payment_form_signature(amount, order_id, currency),
            'i': payment_method,
            'phone': phone,
            'em': email,
            'lang': lang,
        }
        payload = {k: v for k, v in params.items() if v is not None}
        return self.INVOICE_BASE_URL.format(query=urlencode(payload))

    def get_balance(self) -> models.Balance:
        resp = self.request('balance')
        currencies_values = {i['currency']: i.get('value') for i in resp['balance']}
        return models.Balance(**currencies_values)

    # def orders(self, order_id: int = None, payment_id: str = None, order_status: int = None,
    #            date_from: str = None, date_to: str = None, page: int = None):
    #     json = {
    #         'orderId': order_id,
    #         'paymentId': payment_id,
    #         'orderStatus': order_status,
    #         'dateFrom': date_from,
    #         'dateTo': date_to,
    #         'page': page,
    #     }
    #     return self.request('orders', json)
    #
    # def create_order(self, i: int, email: str, ip: str, amount: int, currency: str = 'RUB',
    #                  payment_id: str = None, tel: str = None):
    #     json = {
    #         'i': i,
    #         'email': email,
    #         'ip': ip,
    #         'amount': amount,
    #         'currency': currency,
    #         'paymentId': payment_id,
    #         'tel': tel,
    #     }
    #     return self.request('orders/create', json)
    #
    # def currencies(self):
    #     return self.request('currencies')
    #
    # def currency_status(self, payment_method: int):
    #     return self.request(f'currencies/{payment_method}/status')
    #
    # def shops(self):
    #     return self.request('shops')
