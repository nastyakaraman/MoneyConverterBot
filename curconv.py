#import telebot
import requests
import json
from exceptions import ConvertionException, InputDataException, ServerResponseException
from config import api_key, values, values_plural

class CurrencyConverter():
    @staticmethod
    def currency_converter(from_cur, to_cur, amount_, bot_, message_):
        try:
            #чтобы была правильно введено количество валюты
            if not amount_.isdigit(): #проверяет целые числа
                if '.' or ',' in amount_:  #костыль, чтобы проверить float
                    symbol = '.' or ',' in amount_
                    if not amount_.replace(symbol, '').isdigit():
                        raise InputDataException('Ошибка в количестве валюты')

            if from_cur not in values.keys():
                raise InputDataException('Ошибка в конвертируемой валюте. Бот не работает с этой валютой')

            elif to_cur not in values.keys():
                raise InputDataException('Ошибка в валюте конвертации. Бот не работает с этой валютой')

            TO=values[to_cur]
            FROM=values[from_cur]

            if TO==FROM:
                raise InputDataException('Нельзя конвертировать валюту в ту же валюту')

        except ConvertionException as e:
            bot_.reply_to(message_, f"Не удалось обработать команду \n{e}")

        else:
            r = requests.get(f'https://api.apilayer.com/currency_data/convert?to={TO}&from={FROM}&amount={amount_}', headers={'apikey': api_key})
            try:
                d = json.loads(r.content)
                if 'result' not in d.keys():
                    raise ServerResponseException ('Нет ответа от сервера')
            except ConvertionException as e:
                bot_.reply_to(message_, f"Не удалось обработать команду \n{e}")
            else:
                res=d['result']
                text= (f"{amount_} {values_plural[from_cur]} = {res} {values_plural[to_cur]}")
                return text