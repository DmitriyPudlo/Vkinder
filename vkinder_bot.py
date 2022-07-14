from random import randrange

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = input('Token: ')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
client_id = 0

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
                client_id = event.user_id
                url_api = 'https://api.vk.com/method/users.get'
                params = {'user_ids': client_id,
                          'fields': ('city', 'bdate', 'sex'),
                          'access_token': token,
                          'v': '5.131'}
                response_vk = requests.get(url_api, params=params).json()['response']
                write_msg(event.user_id, f"Твои данные: {response_vk}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")


