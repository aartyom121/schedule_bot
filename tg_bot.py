import datetime
import time
from functools import partial
from threading import Thread
import schedule
import telebot
import json
import schedule_parse


API = '7883465127:AAHoTqZoy_Ciw7-meewkuzIivxdKtdbCQqo'
bot = telebot.TeleBot(API)


def get_schedule():
    schedule_parse.main()
    with open('day_schedule.json', 'r', encoding='utf-8') as file:
        mes = f'<b>Пары на {datetime.date.today()}:</b>\n'
        data_json = file.read()
        data = json.loads(data_json)
        for i, el in enumerate(data):
            mes += f"{i + 1}){el['Name']}\nВремя: {el['studies_time']}\n"
        if mes != '':
            return mes
        else:
            mes = 'Пар нет!'
            return mes


@bot.message_handler(commands=['start'])
def start(message):
    # schedule.every().day.at("13:41").do(send_schedule, message)
    # schedule.every().minute.do(partial(send_schedule, message))

    schedule_thread = Thread(target=run_schedule)
    schedule_thread.start()
    send_schedule(message)


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def send_schedule(message):
    send_mes = get_schedule()
    bot.send_message(message.chat.id, send_mes, parse_mode='html')


def main():
    print("Bot started")
    bot.infinity_polling()


if __name__ == '__main__':
    main()
