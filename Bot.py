from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard


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
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('СТАРТ')
                keyboard = keyboard.get_keyboard()
                self.write_msg(event.user_id, 'Для начала работы нажми одну из кнопок!', keyboard=keyboard)
            return event.user_id

    def speak(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request == "СТАРТ":
                        self.write_msg(event.user_id,
                                       "Сейчас я изучу твой профиль и постараюсь найти для тебя подходящего кандидата!")
                        return
                    elif request == "СЛЕДУЮЩИЙ":
                        self.write_msg(event.user_id, "Сейчас поищу...")
                        return
                    elif request == "ИЗБРАННЫЕ":
                        self.write_msg(event.user_id, "Еще не реализовано")
                        return
                    elif request == "СТОП":
                        self.write_msg(event.user_id, "Пока!")
                        return True

    def response(self, info):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('СЛЕДУЮЩИЙ')
        keyboard.add_button('СТОП')
        keyboard.add_button('ДОБАВИТЬ В ИЗБРАННЫЕ')
        keyboard.add_button('ПОКАЗАТЬ ИЗБРАННЫХ')
        keyboard = keyboard.get_keyboard()
        for event in self.longpoll.listen():
            candidate_info = info[0]
            attachment = info[1]
            self.write_msg(event.user_id, candidate_info, attachment, keyboard=keyboard)
            break

    def ending(self):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('ЗАДАТЬ НОВЫЕ КРИТЕРИИ')
        keyboard.add_button('ПОКАЗАТЬ ИЗБРАННЫХ')
        keyboard = keyboard.get_keyboard()
        for event in self.longpoll.listen():
            self.write_msg(event.user_id, 'Больше никого по заданным критериям не нашел.', keyboard=keyboard)
            break

