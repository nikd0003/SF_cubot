import json
import requests
from config import exchanges, APIKEY


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")
        if base_key == sym_key:
            raise APIException(f'Перевести одинаковые валюты {base} невозможно!')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество {amount} не удалось обработать!')
        url = f"https://api.apilayer.com/currency_data/live?source={base_key}&currencies={sym_key}"
        payload = {}
        headers = {"apikey": APIKEY}
        r = requests.request("GET", url, headers=headers, data=payload)
        print(r.content)
        resp = json.loads(r.content)
        new_price = resp['quotes'][base_key+sym_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message
