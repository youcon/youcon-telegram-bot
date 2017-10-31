from telebot import TeleBot, types
import schedule
import os
from emoji import emojize

bot = TeleBot(os.environ.get("TELEGRAM_TOKEN", None))


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Menu' or message.text == '/start')
def on_start(message):
    text = 'How can I help you?'

    inline = types.InlineKeyboardMarkup()
    inline.add(types.InlineKeyboardButton(text='View the schedule', callback_data='viewSchedule'))
    inline.add(types.InlineKeyboardButton(text='My schedule', callback_data='mySchedule'))
    inline.add(types.InlineKeyboardButton(text='Rate the talk', callback_data='rateTalk'))
    inline.add(types.InlineKeyboardButton(text='Ask a question', callback_data='askQuestion'))

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Menu')

    bot.send_message(message.chat.id, emojize(':vhs:', use_aliases=True), reply_markup=keyboard)
    bot.send_message(message.chat.id, text, reply_markup=inline)


@bot.callback_query_handler(func=lambda call: call.data == 'viewSchedule')
def view_schedule(call):
    text = 'Choose how you prefer to view the schedule:'
    all = types.InlineKeyboardButton(text='All', callback_data='viewSchedule-all')
    by_tracks = types.InlineKeyboardButton(text='By tracks', callback_data='viewSchedule-byTracks')
    markup = types.InlineKeyboardMarkup()
    markup.row(all, by_tracks)
    bot.send_message(call.from_user.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'mySchedule')
def my_schedule(call):
    text = emojize('Here you’ll see the talks you’re interested in. To add a talk here, mark it with :star:'
                   ' while browsing the schedule. I’ll remind you about a featured talk 5 minutes before it starts.',
                   use_aliases=True)
    bot.send_message(call.from_user.id, text)


@bot.callback_query_handler(func=lambda call: call.data == 'rateTalk')
def rate_the_talk(call):
    text = 'Select the track of the talk you’d like to rate.'
    markup = types.InlineKeyboardMarkup()
    for track in schedule.schedule:
        markup.row(types.InlineKeyboardButton(text=track['name'], callback_data='rate-' + track['name']))
    bot.send_message(call.from_user.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'askQuestion')
def ask_question(call):
    text = 'Please type your question or message. I’ll send it to the organizers, ' \
           'and they’ll get back to you on Telegram.'
    bot.send_message(call.from_user.id, text)


@bot.callback_query_handler(func=lambda call: call.data == 'viewSchedule-all')
def get_schedule(call):
    text = 'Demo schedule'
    more = types.InlineKeyboardButton(text='More', callback_data='more')
    fav = types.InlineKeyboardButton(text=emojize(':star:', use_aliases=True), callback_data='fav')
    markup = types.InlineKeyboardMarkup()
    markup.row(more, fav)
    bot.send_message(call.from_user.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'viewSchedule-byTracks')
def get_schedule_by_tracks(call):
    text = 'Choose the track whose schedule you’d like to see.'
    markup = types.InlineKeyboardMarkup()
    for track in schedule.get_all():
        markup.row(types.InlineKeyboardButton(text=track['name'], callback_data='sch-' + track['name']))
    bot.send_message(call.from_user.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('sch-'))
def get_track(call):
    title = call.data.replace('sch-', '')
    try:
        for lecture in schedule.get_track(title)['schedule']:
            time = lecture['time']
            title = lecture['title']
            text = f'***{time}***\n{title}\n'
            if 'speaker' in lecture:
                speaker = lecture['speaker']['name']
                text += f'*{speaker}*\n'

            more = types.InlineKeyboardButton(text='More', callback_data='more')
            fav = types.InlineKeyboardButton(text=emojize(':star:', use_aliases=True), callback_data='fav')
            markup = types.InlineKeyboardMarkup()
            markup.row(more, fav)
            bot.send_message(call.from_user.id, text, parse_mode='MARKDOWN', reply_markup=markup)
    except TypeError as ex:
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith('rate-'))
def get_track_for_rate(call):
    title = call.data.replace('rate-', '')
    try:
        for lecture in schedule.get_track(title)['schedule']:
            time = lecture['time']
            title = lecture['title']
            text = f'***{time}***\n{title}\n'
            if 'speaker' in lecture:
                speaker = lecture['speaker']['name']
                text += f'*{speaker}*\n'

            poo = types.InlineKeyboardButton(text=emojize(':poop:', use_aliases=True), callback_data='poo')
            dislike = types.InlineKeyboardButton(text=emojize(':thumbsdown:', use_aliases=True),
                                                 callback_data='dislike')
            ok = types.InlineKeyboardButton(text=emojize(':ok_hand:', use_aliases=True), callback_data='ok')
            like = types.InlineKeyboardButton(text=emojize(':thumbsup:', use_aliases=True),
                                              callback_data='like')
            heart = types.InlineKeyboardButton(text=emojize(':heart:', use_aliases=True),
                                               callback_data='heart')
            markup = types.InlineKeyboardMarkup()
            markup.row(poo, dislike, ok, like, heart)
            bot.send_message(call.from_user.id, text, parse_mode='MARKDOWN', reply_markup=markup)
    except TypeError as ex:
        return


bot.polling(none_stop=True)
