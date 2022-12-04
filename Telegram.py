import telebot
from telebot import types
import tokens
from VK import VK
import Keyboard
from db import Connector
import config

token_for_tele = f'{tokens.TELEGRAM_TOKEN}'
tele_bot = telebot.TeleBot(token_for_tele)


def create_markup(keyboard):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in keyboard:
        markup.add(key)
    return markup


class Telegram:
    def __init__(self, token):
        self.token = token
        self.is_end_dialog = True
        self.vk = VK(self.token)
        self.connect = Connector()
        self.keyword = Keyboard.Keyword()
        self.user_id = self.vk.get_user_id()
        self.id_candidates = self.vk.search_candidate(self.user_id)
        self.favor_ids = self.connect.show_candidates(self.user_id)
        self.candidate_generator = self.generator(self.id_candidates)
        self.favor_generator = self.generator(self.favor_ids)

    def generator(self, lists):
        cnt1 = 0
        while len(lists) > cnt1:
            if len(lists) == cnt1:
                self.is_end_dialog = False
            yield lists[cnt1]
            cnt1 += 1

    def prepare_info(self, candidate_id):
        response = self.vk.show_candidate(candidate_id)
        photos_ids = self.vk.photos_ids(candidate_id)
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
    def start(self, message):
        tele_bot.send_message(message.chat.id,
                              "Привет! Я помогу тебе найти партнера для знакомств!")
        markup = create_markup(Keyboard.greeting)
        tele_bot.send_message(message.chat.id, 'Для продолжения нажми кнопку ниже!', reply_markup=markup)

    @tele_bot.message_handler(content_types='text')
    def speak(self, message):
        candidate_id = ''
        if message.text == self.keyword.START or message.text == self.keyword.NEXT or message.text == self.keyword.CONTINUE:
            if message.text == self.keyword.CONTINUE:
                tele_bot.send_message(message.chat.id,
                                      'Возвращаемся к просмотру кандидатов')
            else:
                tele_bot.send_message(message.chat.id,
                                      "Сейчас поищу...")
            candidate_id = next(self.candidate_generator)
            to_bot = self.prepare_info(candidate_id)
            tele_bot.send_message(message.chat.id, f'{to_bot}')
            tele_bot.send_message(message.chat.id,
                                  '____________________')
            markup = create_markup(Keyboard.response)
            tele_bot.send_message(message.chat.id, 'Для продолжения нажми кнопку ниже!', reply_markup=markup)
        if message.text == self.keyword.STOP:
            tele_bot.send_message(message.chat.id, "Пока")
            return
        if message.text == self.keyword.ADD_FAVOR:
            photos_ids = self.vk.photos_ids(candidate_id)
            self.connect.add_candidate(self.user_id, candidate_id, photos_ids)
            markup = create_markup(Keyboard.add_favor_key)
            tele_bot.send_message(message.chat.id, "Добавлен в ваш список избранных!", reply_markup=markup)
        if message.text == self.keyword.SHOW_FAVOR or message.text == self.keyword.NEXT_FAVOR:
            favor_id = next(self.favor_generator)
            favor_to_bot = self.prepare_info(favor_id)
            markup = create_markup(config.FAVOR_COMMANDS[self.is_end_dialog])
            if message.text == self.keyword.SHOW_FAVOR:
                tele_bot.send_message(message.chat.id, "Сейчас выведу ваших избранных", reply_markup=markup)
            tele_bot.send_message(message.chat.id, f'{favor_to_bot}', reply_markup=markup)
