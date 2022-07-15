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


class WorkWithGet:
    def __init__(self, token, url_api):
        self.token = token
        self.url_api = url_api


class Client(WorkWithGet):
    def __init__(self, token, url_api, id_user):
        super().__init__(token, url_api)
        self.id_user = id_user


    def search_client_info(self):
        params = {'user_ids': self.id_user,
                  'fields': 'city, sex, bdate',
                  'access_token': self.token,
                  'v': '5.131'}
        response_vk = requests.get(self.url_api, params=params).json()['response']
        return response_vk


class Search(WorkWithGet):
    def __init__(self, token, url_api, search_criteria):
        super().__init__(token, url_api)
        self.search_criteria = search_criteria

    def search_candidate(self):
        params = {'count': 50,
                  'city': self.search_criteria['city'],
                  'sex': self.search_criteria['sex'],
                  'status': 6,
                  'age_from': self.search_criteria['age'],
                  'age_to': self.search_criteria['age'],
                  'has_photo': 1,
                  'access_token': self.token,
                  'v': '5.131'}
        response_vk = requests.get(self.url_api, params=params).json()['response']
        return response_vk

    def url_photo(self):
        pass


if __name__ == '__main__':
    token_for_bot = 'vk1.a.JxoJoWFTReNOLAljFNSnro8hPf-id5kL96fZMNav2GpjCkRyq-nCjfzKZ7Qw0JGLaqvaGkCGxaQd9wu5gFbbe-lJ9SI8V1ylZAU8b5UtHKuyE7LYY7leev62QD56yu9fVwsmYRhSyPDevWqdjI3QwJwIEV_bHqEPQ8i_-Fh-W0OVYQBk4xuPHfDUq9CbMSFD'
    token_for_get = 'vk1.a.91ZpDzsxgBpqsfabik3ZtJXTQmHr_NwlABJc3-NJwylWyWrHEF78HHofS5nTyFeKSe0JmmOU9oKjlBp9gceEjNJFSYYs6Qe25z65hTNUVfrvNLBZMgqHCrqz-nvAgMLZ5_4zLjBVgwfhKpEk7aBAh1-s0-Xq6dFygbEnP17tSAFRSDGmN5hJxqMtlLj3xPKR'
    url_api_for_client = 'https://api.vk.com/method/users.get'
    url_api_for_search = 'https://api.vk.com/method/users.search'
    vk_bot = Bot(token_for_bot)
    while True:
        answer = vk_bot.speak()
        if type(answer) == int:  # and answer not in BD
            client = Client(token_for_get, url_api_for_client, answer)
            print(client.search_client_info())
            x = Search(token_for_get, url_api_for_search, {'city': 108, 'sex': 1, 'age': 25})
            print(x)
