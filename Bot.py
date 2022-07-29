from vk_api.longpoll import VkLongPoll, VkEventType
from BD import show_favor_bd, add_favor
from random import randrange
from VK import VK
import vk_api
import Keyboard


class Bot:
    def __init__(self, token_for_bot, token_for_get):
        self.token_for_bot = token_for_bot
        self.token_for_get = token_for_get
        self.vk = vk_api.VkApi(token=self.token_for_bot)
        self.longpoll = VkLongPoll(self.vk)
        self.get = VK(token_for_get)

    def write_msg(self, user_id, message, attachment=None, keyboard=None):
        self.vk.method('messages.send', {'user_id': user_id,
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
                    if request == "Старт":
                        self.write_msg(event.user_id,
                                       "Сейчас я изучу твой профиль и постараюсь найти для тебя подходящего партнёра!")
                        return

    def speak(self, user_id=None):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request == "Следующий" or request == "Следующий из списка избранных":
                        self.write_msg(event.user_id, "Сейчас поищу...")
                        return
                    elif request == "Добавить в избранные":
                        add_favor(user_id)
                        keyboard = Keyboard.add_favor_key
                        self.write_msg(event.user_id, "Добавлен в ваш список избранных!", keyboard=keyboard)
                        return self.speak()
                    elif request == "Показать избранных":
                        self.write_msg(event.user_id, "Сейчас выведу ваших избранных")
                        return "Показать избранных"
                    elif request == 'Продолжить просмотр кандидатов':
                        self.write_msg(event.user_id, "Возвращаемся к просмотру кандидатов")
                        return 'Продолжить просмотр кандидатов'
                    elif request == "Стоп":
                        self.write_msg(event.user_id, "Пока!")
                        return "Стоп"

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
        self.start()
        while True:
            criteria_search = self.get.search_client_info(client_id)
            candidates_ids = self.get.search_candidate(criteria_search)
            for id_candidate in candidates_ids:
                photos_ids = self.get.photos_ids(id_candidate)
                to_bot = self.get.show_candidate(id_candidate, photos_ids)
                self.response(to_bot)
                self.show_key(Keyboard.response_key)
                command = self.speak(id_candidate)
                if command == "Показать избранных":
                    response_favor = Keyboard.response_favor_key
                    favor_ending = Keyboard.favor_ending_key
                    self.show_favor(response_favor, favor_ending)
                elif command == "Стоп":
                    break
            self.ending()
            self.show_key(Keyboard.ending_key)
            command = self.speak()
            if command == "Показать избранных":
                favor_without_candidates = Keyboard.response_favor_without_candidates_key
                favor_ending_without_candidates = Keyboard.favor_ending_without_candidates_key
                self.show_favor(favor_without_candidates, favor_ending_without_candidates)
            break

    def show_favor(self, key_begin, key_end):
        favor_ids = show_favor_bd()
        for favor_id in favor_ids:
            favor_photos_ids = self.get.photos_ids(favor_id)
            favor_to_bot = self.get.show_candidate(favor_id, favor_photos_ids)
            self.response_favor(favor_to_bot)
            self.show_key(key_begin)
            answer = self.speak()
            if answer == 'Продолжить просмотр кандидатов':
                return
        self.favor_ending()
        self.show_key(key_end)
        return self.speak()
