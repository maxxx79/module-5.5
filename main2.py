import telebot

from config3 import *
from extensions import Converter, ApiExeption



bot = telebot.TeleBot(TOK)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '       Чтобы начать работу,\n введи команду боту через пробел:' \
           '\n\n <имя валюты> ' \
           '\n\n <в какую валюту перевести> ' \
           '\n\n <количество переводимой валюты>'
    text2 = '<Увидеть список ' \
            'всех доступных валют: /values >'
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, text2)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, 'Неверное количество параметров!')
    try:
        new_price = Converter.get_price(base, sym, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {sym} : {new_price}")
    except ApiExeption as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")

bot.polling()