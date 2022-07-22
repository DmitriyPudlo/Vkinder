from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class Bot:
    def __init__(self, token):
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message, *attachment):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7),
                                         'attachment': attachment})

    def speak(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request == "Start":
                        self.write_msg(event.user_id,
                                       "Сейчас я изучу твой профиль и постараюсь найти для тебя подходящего кандидата!")
                        return event.user_id
                    elif request == "Стоп":
                        self.write_msg(event.user_id,
                                       "Пока!")
                        break
                    elif request == "Следующий":
                        self.write_msg(event.user_id,
                                       "Сейчас поищу...")
                        break
                    else:
                        self.write_msg(event.user_id,
                                       "Не понял вашего ответа... Если не знаете что делать, наберите 'Help'")

    def response(self, info):
        for event in self.longpoll.listen():
            self.write_msg(event.user_id, info[1])
            for id_photo in info[2]:
                self.write_msg(event.user_id, 'Фотография:', id_photo)
            break
