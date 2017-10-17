import config
import telebot
import schedule

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def on_start(message):
    text = 'Расписание масштабной конференции для ИТ специалистов в Саратове'
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Технический трек 1', 'Технический трек 2')
    markup.row('Технический трек 3', 'Технический трек 4')
    markup.row('Бизнес трек')
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=["text"])
def on_text(message):
    try:
        text = ''
        for lecture in schedule.get_track(message.text)['schedule']:
            time = lecture['time']
            title = lecture['title']
            text += f'***{time}***\n{title}\n'
            if 'speaker' in lecture:
                speaker = lecture['speaker']['name']
                text += f'*{speaker}*\n'
            text += '\n'

        bot.send_message(message.chat.id, text, parse_mode='MARKDOWN')
    except TypeError as ex:
        return


if __name__ == '__main__':
    bot.polling(none_stop=True)
