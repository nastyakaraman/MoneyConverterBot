import telebot
from exceptions import ConvertionException, InputDataException, ServerResponseException
from config import TOKEN, values
from curconv import CurrencyConverter

bot = telebot.TeleBot(TOKEN)

#bot.send_message()
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}.\n\nЧтобы воспользоваться ботом, напиши:\n\
<название твоей валюты> <название валюты, в которую ты хочешь конвертировать средства>\
 <количество конвертируемой валюты>\n\nНапример: доллар рубль 100\n\nВалюту указывай в единственном числе!\n\nДля отображения доступных для конвертации валют, используй команду /value")

@bot.message_handler(commands=['value'])
def send_values(message):
    #bot.send_message(message.chat.id, values.keys())
    bot.send_message(message.chat.id, values['вывод'])

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        inputdata=message.text.split(' ')
        if len(inputdata)!=3:
            raise InputDataException('Необходимо ввести три параметра, попробуйте еще раз')
    except ConvertionException as e:
        bot.reply_to(message, f"Не удалось обработать команду \n{e}")
    else:
        fromcur, tocur, amount = message.text.split(' ')
        fromcur, tocur = fromcur.lower(), tocur.lower() #заменяет все на строчные буквы на всякий случай
        try:
            result = CurrencyConverter.currency_converter(fromcur, tocur, amount, bot, message)
        except ConvertionException as e:
            bot.reply_to(message, f"Не удалось обработать команду \n{e}")
        except Exception as e:
            bot.reply_to(message, f"Не удалось обработать команду \n{e}")
        else:
            bot.reply_to(message, result)

bot.polling(none_stop=True)