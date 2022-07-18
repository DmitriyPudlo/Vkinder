import requests
from vkinder_bot import Bot

COUNT_CANDIDATE = 50
IN_SEARCH = 6
WITH_PHOTO = 1


class WorkWithGet:
    def __init__(self, token):
        self.token = token
        self.host = 'https://api.vk.com/method'

    def search_client_info(self, user_id):
        params = {'user_ids': user_id,
                  'fields': 'city, sex, bdate',
                  'access_token': self.token,
                  'v': '5.131'}
        response_vk = requests.get(f'{self.host}/users.get', params=params).json()['response']
        return response_vk

    def search_candidate(self, criteria):
        params = {'count': COUNT_CANDIDATE,
                  'city': criteria['city'],
                  'sex': criteria['sex'],
                  'status': IN_SEARCH,
                  'age_from': criteria['age'],
                  'age_to': criteria['age'],
                  'has_photo': WITH_PHOTO,
                  'access_token': self.token,
                  'v': '5.131'}
        response_vk = requests.get(f'{self.host}/users.search', params=params).json()['response']
        return response_vk


if __name__ == '__main__':
    token_for_bot = ''
    token_for_get = ''
    vk_bot = Bot(token_for_bot)
    answer = vk_bot.speak()
    get = WorkWithGet(token_for_get)
    while True:
        answer = vk_bot.speak()
        if type(answer) == int:  # and answer not in BD
            search_criteria = get.search_client_info(answer)


