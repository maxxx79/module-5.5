import requests
import json
from config3 import exchanges

class ApiExeption(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return ApiExeption(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise ApiExeption(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise ApiExeption(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ApiExeption(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest{base_key}&symbols={sym_key}")

        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * float(amount)
        return round(new_price, 2)


  #      r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base_key}&symbols={sym_key}")
  #      resp = json.loads(r.content)
  #      new_price = resp['rates'][sym_key] * amount
  #      new_price = round(new_price, 3)
  #      message = f"Цена {amount} {base} в {sym} : {new_price}"
  #      return message