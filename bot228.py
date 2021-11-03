from pyowm import OWM
import telebot
from telebot.types import Message

owm = OWM("e1b9dd31f0d4c906e723b1cb2dfc4fb3")

token = '2094805370:AAFf1jRKeQa2ZpFvRDkHDv1wnHhOLgRtLFU'


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "hi, i am weather bot")
    bot.send_message(message.chat.id, "enter your city")


@bot.message_handler(content_types=['text'])
def next(message):

    if message.text.lower():
        place = message.text

        srch = owm.weather_manager()

        let = srch.weather_at_place(place)

        show = let.weather

        tAll = show.temperature('celsius')

        info = tAll['temp']

        bot.send_message(message.chat.id, 'Curent temperature in')
        bot.send_message(message.chat.id, message.text)
        bot.send_message(message.chat.id, 'is')
        bot.send_message(message.chat.id, info)

        print(message.text)

    else:
        bot.send_message(message.chat.id, 'enter correct city')


bot.infinity_polling()


input('end')
