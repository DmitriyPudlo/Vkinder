import telebot
from telebot import types
import tokens
from VK import VK
import Keyboard
from db import Connector
import config

token_for_tele = f'{tokens.TELEGRAM_TOKEN}'
token_for_get = f'{tokens.GET_TOKEN}'
tele_bot = telebot.TeleBot(token_for_tele)
keyword = Keyboard.Keyword()


def create_markup(keyboard):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in keyboard:
        markup.add(key)
    return markup


def show_candidate():
    try:
        telegram.candidate_id = next(telegram.candidate_generator)
        photo_ids = telegram.connect.show_photo(telegram.candidate_id)
        to_bot = telegram.prepare_info(telegram.candidate_id, photo_ids)
        markup = create_markup(Keyboard.response)
        return {'to_bot': to_bot, 'markup': markup}
    except StopIteration:
        markup = create_markup(Keyboard.ending)
        return {'to_bot': 'Больше никого по заданным критериям не нашел', 'markup': markup}


class Telegram:
    def __init__(self, token):
        self.token = token
        self.is_end_dialog = True
        self.vk = VK(self.token)
        self.connect = Connector()
        self.user_id = self.vk.get_user_id()
        self.id_candidates = self.vk.search_candidate(self.user_id)
        self.favor_ids = self.connect.show_candidates(self.user_id)
        self.candidate_generator = self.generator(self.id_candidates)
        self.candidate_id = ''

    def generator(self, lists):
        cnt1 = 0
        while len(lists) > cnt1:
            if len(lists) == cnt1:
                self.is_end_dialog = False
            yield lists[cnt1]
            cnt1 += 1

    def prepare_info(self, candidate_id, photos_ids=None):
        print(candidate_id)
        response = self.vk.show_candidate(candidate_id)
        if photos_ids is None:
            photos_ids = self.connect.show_photo(candidate_id)
        first_name = response['first_name']
        last_name = response['last_name']
        url = f'https://vk.com/id{candidate_id}'
        photos_url = [f'https://vk.com/photo{candidate_id}_{photo_id}' for photo_id in photos_ids]
        photos_url = ', '.join(photos_url)
        info = f'''Имя: {first_name} {last_name},
    Ссылка на её профиль: {url},
    Самые популярные фотографии: {photos_url}'''
        return info


@tele_bot.message_handler(commands=['start'])
def start(message):
    tele_bot.send_message(message.chat.id,
                          "Привет! Я помогу тебе найти партнера для знакомств!")
    markup = create_markup(Keyboard.greeting)
    tele_bot.send_message(message.chat.id, 'Для продолжения нажми кнопку ниже!', reply_markup=markup)


@tele_bot.message_handler(func=lambda message: message.text == keyword.STOP)
def say_bay(message):
    tele_bot.send_message(message.chat.id, "Пока")
    tele_bot.stop_polling()


@tele_bot.message_handler(func=lambda message: message.text == keyword.ADD_FAVOR)
def add_favor(message):
    photos_ids = telegram.vk.photos_ids(telegram.candidate_id)
    telegram.connect.add_candidate(telegram.user_id, telegram.candidate_id, photos_ids)
    markup = create_markup(Keyboard.add_favor)
    tele_bot.send_message(message.chat.id, "Добавлен в ваш список избранных!", reply_markup=markup)


@tele_bot.message_handler(func=lambda message: message.text == keyword.SHOW_FAVOR)
def show_favor(message):
    buttons = config.FAVOR_COMMANDS[telegram.is_end_dialog]
    markups_end = create_markup(buttons)
    tele_bot.send_message(message.chat.id, "Сейчас выведу ваших избранных")
    for favor_id in telegram.favor_ids:
        favor_to_bot = telegram.prepare_info(favor_id)
        tele_bot.send_message(message.chat.id, f'{favor_to_bot}')
    tele_bot.send_message(message.chat.id, 'Избранных больше нет', reply_markup=markups_end)


@tele_bot.message_handler(func=lambda message: message.text == keyword.START)
def start(message):
    tele_bot.send_message(message.chat.id, "Сейчас поищу...")
    info = show_candidate()
    tele_bot.send_message(message.chat.id, f'{info["to_bot"]}')
    tele_bot.send_message(message.chat.id, '____________________')
    tele_bot.send_message(message.chat.id, 'Для продолжения нажми кнопку ниже!', reply_markup=info["markup"])


@tele_bot.message_handler(func=lambda message: message.text == keyword.NEXT)
def next_candidate(message):
    tele_bot.send_message(message.chat.id, "Сейчас поищу...")
    info = show_candidate()
    tele_bot.send_message(message.chat.id, f'{info["to_bot"]}')
    tele_bot.send_message(message.chat.id, '____________________')
    tele_bot.send_message(message.chat.id, 'Для продолжения нажми кнопку ниже!', reply_markup=info["markup"])


@tele_bot.message_handler(func=lambda message: message.text == keyword.CONTINUE)
def continue_browsing(message):
    tele_bot.send_message(message.chat.id, 'Возвращаемся к просмотру кандидатов')
    info = show_candidate()
    tele_bot.send_message(message.chat.id, f'{info["to_bot"]}')
    tele_bot.send_message(message.chat.id, '____________________')
    tele_bot.send_message(message.chat.id, 'Для продолжения нажми кнопку ниже!', reply_markup=info["markup"])


if __name__ == '__main__':
    telegram = Telegram(token_for_get)
