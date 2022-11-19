import telebot
from telebot import types
import tokens
from VK import VK
import Keyboard
from db import Connector
import config

token_for_get = f'{tokens.GET_TOKEN}'
token_for_tele = f'{tokens.TELEGRAM_TOKEN}'
tele_bot = telebot.TeleBot(token_for_tele)
keyword = Keyboard.Keyword()


class Telegram:
    def __init__(self, token):
        self.token = token
        self.tele_bot = telebot.TeleBot(token_for_tele)
        self.is_end_dialog = True

    def flat_generator(self, lists):
        cnt1 = 0
        while len(lists) > cnt1:
            if len(lists) == cnt1:
                self.is_end_dialog = False
            yield lists[cnt1]
            cnt1 += 1


def create_markup(keyboard):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in keyboard:
        markup.add(key)
    return markup


def prepare_info(candidate_id):
    response = vk.show_candidate(candidate_id)
    photos_ids = vk.photos_ids(candidate_id)
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


@tele_bot.message_handler(content_types='text')
def speak(message):
    candidate_id = ''
    if message.text == keyword.START or message.text == keyword.NEXT or message.text == keyword.CONTINUE:
        if message.text == keyword.CONTINUE:
            tele_bot.send_message(message.chat.id,
                                  'Возвращаемся к просмотру кандидатов')
        else:
            tele_bot.send_message(message.chat.id,
                                  "Сейчас поищу...")
        candidate_id = next(candidate_generator)
        to_bot = prepare_info(candidate_id)
        tele_bot.send_message(message.chat.id, f'{to_bot}')
        tele_bot.send_message(message.chat.id,
                              '____________________')
        markup = create_markup(Keyboard.response)
        tele_bot.send_message(message.chat.id, 'Для продолжения нажми кнопку ниже!', reply_markup=markup)
    if message.text == keyword.STOP:
        tele_bot.send_message(message.chat.id, "Пока")
        return
    if message.text == keyword.ADD_FAVOR:
        photos_ids = vk.photos_ids(candidate_id)
        connect.add_candidate(user_id, candidate_id, photos_ids)
        markup = create_markup(Keyboard.add_favor_key)
        tele_bot.send_message(message.chat.id, "Добавлен в ваш список избранных!", reply_markup=markup)
    if message.text == keyword.SHOW_FAVOR or message.text == keyword.NEXT_FAVOR:
        favor_id = next(favor_generator)
        favor_to_bot = prepare_info(favor_id)
        markup = create_markup(config.FAVOR_COMMANDS[telegram.is_end_dialog])
        if message.text == keyword.SHOW_FAVOR:
            tele_bot.send_message(message.chat.id, "Сейчас выведу ваших избранных", reply_markup=markup)
        tele_bot.send_message(message.chat.id, f'{favor_to_bot}', reply_markup=markup)


vk = VK(token_for_get)
user_id = vk.get_user_id()
telegram = Telegram(token_for_get)
id_candidates = vk.search_candidate(user_id)
candidate_generator = telegram.flat_generator(id_candidates)
connect = Connector()
favor_ids = connect.show_candidates(user_id)
favor_generator = telegram.flat_generator(favor_ids)
tele_bot.polling(none_stop=True)
