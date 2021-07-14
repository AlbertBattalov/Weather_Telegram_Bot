import telebot
import random
import requests
import time

from telebot.types import Message
API_key_weather = 'f718ac5f2a80fc4f9aa7e6adf79d9e16'
API_URL = 'https://api.openweathermap.org/data/2.5/weather'
TOKEN = '1498660107:AAHY91sRo7uCIsWth3LcHWj7R2_vnlga88w'
bot = telebot.TeleBot(TOKEN)
find_city = ''
smiles = ['*улыбается*', '*радуется*', '*злится*', '*кокетничает*', '*грустит*','*шлет воздушный поцелуй*','*удивляется*','*умиляется*',' *злорадствует*',]
def get_result_weather():
        parameters = {
            'appid': API_key_weather,
            'q': find_city,
            "units": "metric",
            "lang": 'ru'
        }
        r = requests.get(API_URL, params=parameters)
        weather = r.json()
        return (get_data(weather))


def get_data(weather):
    try:
        city = weather['name']
        country = weather['sys']['country']
        temperature = weather['main']['temp']
        press = weather['main']['pressure']
        humidity = weather['main']['humidity']
        wind = weather['wind']['speed']
        desc = weather['weather'][0]['description']
        sunrise = weather['sys']['sunrise']
        sunset = weather['sys']['sunset']
        sunrise_local = time.localtime(sunrise)
        sunset_local = time.localtime(sunset)
        sunrise_normal = time.strftime('%H:%M:%S', sunrise_local)
        sunset_normal = time.strftime('%H:%M:%S', sunset_local)
        return f'Местоположение: {city},{country} \n Температура: {temperature} по Цельсию\nАтомсферное давление: {press}\nВлажность воздуха: {humidity}\nСкорость ветра: {wind} м/с\nОбщее описание погоды: {desc}\nВосход солнца: {sunrise_normal}\nЗакат солнца: {sunset_normal}\n'
    except:
        return "Нет данных о погоде в данном городе"



@bot.message_handler (commands =['start'] )
def send_welcome (message):
    bot.reply_to(message, 'Спасибо, что поздоровались со мной. Я очень эмоциональный и нестабильный психически бот, поэтому буду отвечать эмоциями. Ну же, напишите мне что-нибудь!')
@bot.message_handler (commands =['help'] )
def send_welcome (message):
    bot.reply_to(message, 'Если Вам нужна помощь,то напишите моему создателю @battalb')
#@bot.message_handler(func=lambda message:True)
#def lower (message: Message):
   # bot.reply_to(message , random.choice(smiles))

@bot.message_handler(func=lambda message: True, content_types=['text'])
def Weather(message):
    if message.text == '/weather':
        bot.send_message(message.from_user.id, "Погода в каком городе Вас интересует?")
        global find_city
        find_city = message.text
        bot.register_next_step_handler(message, get_result)
        print(get_result_weather())
    else:
        bot.send_message(message.from_user.id, 'Неверно совершен запрос.Введите название города. ')
def get_result(message):
    answer = get_result_weather()
    bot.send_message(message.chat.id, answer)
    print(answer)
bot.polling()