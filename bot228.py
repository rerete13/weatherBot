from types import resolve_bases
from bs4 import BeautifulSoup as BS
import requests
import telebot
from telebot.types import Message, Update
from telebot import types
from datetime import date, timedelta


token = '2146536465:AAFYI6XOYxHSBXhrCFXxoxtoM81sF_XAN-o'
bot = telebot.TeleBot(token)


days0 = 0
days1 = 1
days2 = 2
days3 = 3


@bot.message_handler(commands=['start'])
def start_message(message):

    bot.send_message(message.chat.id, "Привіт, введи своє місто")


@bot.message_handler(content_types=['text'])
def next(message):

    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton(text='завтра', callback_data='1')
    btn2 = types.InlineKeyboardButton(text='після завтра', callback_data='2')
    btn3 = types.InlineKeyboardButton(
        text='після після завтра', callback_data='3')

    markup.add(btn1, btn2, btn3)

    if message.text.lower():

        city = message.text

        def parser(city, days):

            day = date.today()
            day = day + timedelta(days)

            url1 = f'https://ua.sinoptik.ua/погода-{city}/{day}'

            r = requests.get(url1)

            html = BS(r.content, 'lxml')

            return html

        all = []

        all = parser(city, days0).find_all('td', class_='p5')

        try:
            temp = (all[2].text)
            feelLike = (all[3].text)
            wind = float(all[6].text)
            rain = all[7].text

        except IndexError:
            bot.send_message(
                message.chat.id, 'Ви ввели назву міста не українською мовою, або назву неіснуючого міста')

            return

        rep = ['-']

        for i in rep:
            if i in rain:
                rain = rain.replace(i, str(0))

        rainInfo = rain

        rainInfo = float(rainInfo)

        windInfo = wind

        def ifRain(rainInfo):

            if rainInfo == '-':
                rainInfoEnd = 'не передбачуються'

            if rainInfo == 0:
                rainInfoEnd = 'не передбачуються'

            if rainInfo <= 20:
                rainInfoEnd = 'не передбачуються'

            if rainInfo >= 30:
                rainInfoEnd = 'Можливі опади'

            elif rainInfo >= 50:
                rainInfoEnd = 'Присутні опади'

            return rainInfoEnd

        def ifWind(windInfo):

            if windInfo <= 8:
                windInfoEnd = 'слабкий'

            if windInfo >= 8:
                windInfoEnd = 'середній'

            elif windInfo >= 15:
                windInfoEnd = 'сильний'

            return windInfoEnd

        bot.send_message(
            message.chat.id, f'Погода сьогодні:\nТемпература: {temp} \nВідчувається як: {feelLike} \nВітер: {ifWind(windInfo)}\nОпади: {ifRain(rainInfo)}', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):

        if call.message:

            if call.data == '1':

                if call.message.text.lower():

                    city = message.text

                    all = []

                    all = parser(city, days1).find_all('td', class_='p5')

                    temp = (all[2].text)
                    feelLike = (all[3].text)
                    wind = float(all[6].text)
                    rain = all[7].text

                    rainInfo = rain
                    rainInfo = float(rainInfo)
                    windInfo = wind

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                          text=f'Температура: {temp} \nВідчувається як: {feelLike} \nВітер: {ifWind(windInfo)}\nОпади: {ifRain(rainInfo)}')
                return

        if call.message:

            if call.data == '2':

                if call.message.text.lower():

                    city = message.text

                    all = []

                    all = parser(city, days2).find_all('td', class_='p3')

                    temp = (all[2].text)
                    feelLike = (all[3].text)
                    wind = float(all[6].text)
                    rain = all[7].text

                    rainInfo = rain
                    rainInfo = float(rainInfo)
                    windInfo = wind

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                          text=f'Температура: {temp} \nВідчувається як: {feelLike} \nВітер: {ifWind(windInfo)}\nОпади: {ifRain(rainInfo)}')

                return

        if call.message:

            if call.data == '3':

                if call.message.text.lower():

                    city = message.text

                    all = []

                    all = parser(city, days2).find_all('td', class_='p3')

                    temp = (all[2].text)
                    feelLike = (all[3].text)
                    wind = float(all[6].text)
                    rain = all[7].text

                    rainInfo = rain

                    rainInfo = float(rainInfo)

                    windInfo = wind

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                          text=f'Температура: {temp} \nВідчувається як: {feelLike} \nВітер: {ifWind(windInfo)}\nОпади: {ifRain(rainInfo)}')

                return


bot.infinity_polling()
