import requests
from Bot import Bot
from datetime import date, datetime
import time


COUNT_CANDIDATE = 50
ALL_PHOTO = 1000
IN_SEARCH = 6
WITH_PHOTO = 1
TYPE_ALBUM = 'profile'
COUNT_PHOTO = 3


def calculate_age(born):
    born_obj = datetime.strptime(born, '%d.%m.%Y')
    today = date.today()
    return today.year - born_obj.year - ((today.month, today.day) < (born_obj.month, born_obj.day))


def check_status(user_id):
    time.sleep(0.2)
    params = {'user_ids': user_id,
              'access_token': token_for_get,
              'v': '5.131'}
    requests_json = requests.get('https://api.vk.com/method/users.get', params=params).json()
    response = requests_json['response']
    response_open = response[0]
    is_closed = response_open['is_closed']
    if not is_closed:
        return True


class VK:
    def __init__(self, token):
        self.token = token
        self.host = 'https://api.vk.com/method'

    def search_client_info(self, user_id):
        check_sex = {1: 2, 2: 1}
        params = {'user_ids': user_id,
                  'fields': 'city, sex, bdate',
                  'access_token': self.token,
                  'v': '5.131'}
        requests_json = requests.get(f'{self.host}/users.get', params=params).json()
        response = requests_json['response']
        response_open = response[0]
        criteria_search = {'city': response_open['city']['id'],
                           'sex': check_sex[response_open['sex']],
                           'age': calculate_age(response_open['bdate'])}
        return criteria_search

    def search_candidate(self, criteria):
        params = {'count': COUNT_CANDIDATE,
                  'city': criteria['city'],
                  'sex': criteria['sex'],
                  'status': IN_SEARCH,
                  'age_from': criteria['age'],
                  'age_to': criteria['age'],
                  'has_photo': WITH_PHOTO,
                  'access_token': self.token,
                  'is_closed': False,
                  'v': '5.131'}
        requests_json = requests.get(f'{self.host}/users.search', params=params).json()
        response = requests_json['response']
        infos = response['items']
        candidates_ids = [info['id'] for info in infos if check_status(info['id'])]
        return candidates_ids

    def url_photo(self, candidate_id):
        params = {'owner_id': candidate_id,
                  'album_id': TYPE_ALBUM,
                  'count': ALL_PHOTO,
                  'extended': True,
                  'access_token': self.token,
                  'v': '5.131'}
        requests_json = requests.get(f'{self.host}/photos.get', params=params).json()
        response = requests_json['response']
        infos = response['items']
        infos = sorted(infos, reverse=True, key=lambda item: item['likes']['count'])
        urls_photo = [info['sizes'][-1]['url'] for info in infos[:COUNT_PHOTO]]
        return urls_photo


if __name__ == '__main__':
    token_for_bot = ''
    token_for_get = ''
    vk_bot = Bot(token_for_bot)
    answer = vk_bot.speak()
    get = VK(token_for_get)
    while True:
        answer = vk_bot.speak()
        if type(answer) == int:  # and answer not in BD
            search_criteria = get.search_client_info(answer)
