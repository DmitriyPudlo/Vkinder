from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import Keyboard
from BD import add_favor, show_favor


class Bot:
    def __init__(self, token):
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message, attachment=None, keyboard=None):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7),
                                         'attachment': attachment,
                                         'keyboard': keyboard})

    def greeting(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.USER_TYPING:
                keyboard = Keyboard.greeting_key()
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

    def speak(self, user_id):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request == "Следующий" or request == "Следующий из списка избранных":
                        self.write_msg(event.user_id, "Сейчас поищу...")
                        return
                    elif request == "Добавить в избранные":
                        add_favor(user_id)
                        keyboard = Keyboard.add_favor_key()
                        self.write_msg(event.user_id, "Добавлен в ваш список избранных!", keyboard=keyboard)
                        return self.speak(user_id)
                    elif request == "Показать избранных":
                        self.write_msg(event.user_id, "Сейчас выведу ваших избранных")
                        return "Показать избранных"
                    elif request == 'Продолжить просмотр кандидатов':
                        self.write_msg(event.user_id, "Возвращаемся к просмотру кандидатов")
                        return 'Продолжить'
                    elif request == "Стоп":
                        self.write_msg(event.user_id, "Пока!")
                        return "Стоп"

    def response(self, info):
        keyboard = Keyboard.response_key()
        for event in self.longpoll.listen():
            candidate_info = info[0]
            attachment = info[1]
            self.write_msg(event.user_id, candidate_info, attachment)
            self.write_msg(event.user_id, '____________________', keyboard=keyboard)
            break

    def response_favor(self, info):
        keyboard = Keyboard.response_favor()
        for event in self.longpoll.listen():
            candidate_info = info[0]
            attachment = info[1]
            self.write_msg(event.user_id, candidate_info, attachment, keyboard=keyboard)
            break

    def ending(self):
        keyboard = Keyboard.ending_key()
        for event in self.longpoll.listen():
            self.write_msg(event.user_id, 'Больше никого по заданным критериям не нашел', keyboard=keyboard)
            return self.speak(event.user_id)

    def favor_ending(self):
        keyboard = Keyboard.favor_ending_key()
        for event in self.longpoll.listen():
            self.write_msg(event.user_id, 'Избранных больше нет', keyboard=keyboard)
            return self.speak(event.user_id)

