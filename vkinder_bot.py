from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType



class Bot:
    def __init__(self, token):
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def speak(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request == "Start":
                        self.write_msg(event.user_id,
                                       "Сейчас я изучу твой профиль и постараюсь найти для тебя подходящего кандидата!")
                        return event.user_id
                    else:
                        self.write_msg(event.user_id,
                                       "Не понял вашего ответа... Если не знаете что делать, наберите 'Help'")
