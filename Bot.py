from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from VK import VK
from db import Connector
import vk_api
import Keyboard


def prepare_info(candidate_id, response, photos_ids):
    address = {1: 'её', 2: 'его'}
    first_name = response['first_name']
    last_name = response['last_name']
    sex = response['sex']
    name = f'''Имя кандидата: {first_name} {last_name}
               Ссылка на {address[sex]} профиль: https://vk.com/id{candidate_id}'''
    attachments = [f'photo{candidate_id}_{photo_id}' for photo_id in photos_ids]
    attachments = ','.join(attachments)
    return name, attachments


class Bot:
    def __init__(self, token_for_bot, token_for_get):
        self.token_for_bot = token_for_bot
        self.token_for_get = token_for_get
        self.vk_api = vk_api.VkApi(token=self.token_for_bot)
        self.longpoll = VkLongPoll(self.vk_api)
        self.vk = VK(token_for_get)
        self.connect = Connector()
        self.connect.create_database()
        self.keyword = Keyboard.Keyword()

    def write_msg(self, user_id, message, attachment=None, keyboard=None):
        self.vk_api.method('messages.send', {'user_id': user_id,
                                             'message': message,
                                             'random_id': randrange(10 ** 7),
                                             'attachment': attachment,
                                             'keyboard': keyboard})

    def greeting(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.USER_TYPING:
                keyboard = Keyboard.greeting_key
                self.write_msg(event.user_id, 'Для начала работы нажми одну из кнопок!', keyboard=keyboard)
            return event.user_id

    def start(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request == self.keyword.START:
                        self.write_msg(event.user_id,
                                       "Сейчас я изучу твой профиль и постараюсь найти для тебя подходящего партнёра!")
                        return

    def speak(self, user_id=None, photos_id=None):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request == self.keyword.NEXT or request == self.keyword.NEXT_FAVOR:
                        self.write_msg(event.user_id, "Сейчас поищу...")
                        return
                    elif request == self.keyword.ADD_FAVOR:
                        self.connect.add_candidate(event.user_id, user_id)
                        for photo_id in photos_id:
                            self.connect.add_photo(user_id, photo_id)
                        keyboard = Keyboard.add_favor_key
                        self.write_msg(event.user_id, "Добавлен в ваш список избранных!", keyboard=keyboard)
                        return self.speak()
                    elif request == self.keyword.SHOW_FAVOR:
                        self.write_msg(event.user_id, "Сейчас выведу ваших избранных")
                        return self.keyword.SHOW_FAVOR
                    elif request == self.keyword.CONTINUE:
                        self.write_msg(event.user_id, "Возвращаемся к просмотру кандидатов")
                        return self.keyword.CONTINUE
                    elif request == self.keyword.STOP:
                        self.write_msg(event.user_id, "Пока!")
                        return self.keyword.STOP

    def response(self, info):
        for event in self.longpoll.listen():
            candidate_info = info[0]
            attachment = info[1]
            self.write_msg(event.user_id, candidate_info, attachment)
            return

    def response_favor(self, info):
        for event in self.longpoll.listen():
            candidate_info = info[0]
            attachment = info[1]
            self.write_msg(event.user_id, candidate_info, attachment)
            return

    def ending(self):
        for event in self.longpoll.listen():
            self.write_msg(event.user_id, 'Больше никого по заданным критериям не нашел')
            return

    def favor_ending(self):
        for event in self.longpoll.listen():
            self.write_msg(event.user_id, 'Избранных больше нет')
            return

    def show_key(self, keyboard):
        for event in self.longpoll.listen():
            self.write_msg(event.user_id, '____________________', keyboard=keyboard)
            return

    def bot_start(self):
        client_id = self.greeting()
        self.connect.add_client(client_id)
        self.start()
        while True:
            candidates_ids = self.vk.search_candidate(client_id)
            for id_candidate in candidates_ids:
                photos_ids = self.vk.photos_ids(id_candidate)
                response = self.vk.show_candidate(id_candidate)
                to_bot = prepare_info(id_candidate, response, photos_ids)
                self.response(to_bot)
                self.show_key(Keyboard.response_key)
                command = self.speak(id_candidate, photos_ids)
                if command == self.keyword.SHOW_FAVOR:
                    response_favor = Keyboard.response_favor_key
                    favor_ending = Keyboard.favor_ending_key
                    self.show_favor(response_favor, favor_ending, client_id)
                elif command == self.keyword.STOP:
                    break
            self.ending()
            self.show_key(Keyboard.ending_key)
            command = self.speak()
            if command == self.keyword.SHOW_FAVOR:
                favor_without_candidates = Keyboard.response_favor_without_candidates_key
                favor_ending_without_candidates = Keyboard.favor_ending_without_candidates_key
                self.show_favor(favor_without_candidates, favor_ending_without_candidates, client_id)
            self.connect.connect_close()
            break

    def show_favor(self, key_begin, key_end, client_id):
        favor_ids = self.connect.show_candidates(client_id)
        for favor_id in favor_ids:
            favor_photos_ids = self.connect.show_photo(favor_id)
            response = self.vk.show_candidate(favor_id)
            favor_to_bot = prepare_info(favor_id, response, favor_photos_ids)
            self.response_favor(favor_to_bot)
            self.show_key(key_begin)
            answer = self.speak()
            if answer == self.keyword.CONTINUE:
                return
        self.favor_ending()
        self.show_key(key_end)
        return self.speak()

