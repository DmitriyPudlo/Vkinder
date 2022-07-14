from random import randrange
import requests
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
                                       f"Сейчас я изучу твой профиль и постараюсь найти для тебя подходящего кандидата!")
                        return event.user_id
                    elif request == "Help":
                        pass
                    else:
                        self.write_msg(event.user_id,
                                       "Не понял вашего ответа... Если не знаете что делать, наберите 'Help'")


class Client:
    def __init__(self, id_user, token, url_api):
        self.id_user = id_user
        self.token = token
        self.url_api = url_api

    def search_client_info(self):
        params = {'user_ids': self.id_user,
                  'fields': 'city, sex, bdate',
                  'access_token': self.token,
                  'v': '5.131'}
        response_vk = requests.get(self.url_api, params=params).json()['response']
        return response_vk


if __name__ == '__main__':
    token = 'vk1.a.JxoJoWFTReNOLAljFNSnro8hPf-id5kL96fZMNav2GpjCkRyq-nCjfzKZ7Qw0JGLaqvaGkCGxaQd9wu5gFbbe-lJ9SI8V1ylZAU8b5UtHKuyE7LYY7leev62QD56yu9fVwsmYRhSyPDevWqdjI3QwJwIEV_bHqEPQ8i_-Fh-W0OVYQBk4xuPHfDUq9CbMSFD'
    url_api = 'https://api.vk.com/method/users.get'
    vk_bot = Bot(token)
    while True:
        answer = vk_bot.speak()
        if type(answer) == int:  # and answer not in BD
            client = Client(answer, token, url_api)
            print(client.search_client_info())
