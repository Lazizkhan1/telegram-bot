import json
import requests

response_all = requests.get("https://nbu.uz/uz/exchange-rates/json/").text
response = json.loads(response_all)


def get_currency(currency: str) -> dict:
    for i in response:
        if i['code'] == currency:
            return i
