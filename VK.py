import requests
from datetime import date, datetime


COUNT_CANDIDATE = 15
ALL_PHOTO = 1000
IN_SEARCH = 6
WITH_PHOTO = 1
TYPE_ALBUM = 'profile'
COUNT_PHOTO = 3


def calculate_age(born):
    born_obj = datetime.strptime(born, '%d.%m.%Y')
    today = date.today()
    return today.year - born_obj.year - ((today.month, today.day) < (born_obj.month, born_obj.day))


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
                  'age_from': criteria['age'] - 3,
                  'age_to': criteria['age'] + 3,
                  'has_photo': WITH_PHOTO,
                  'access_token': self.token,
                  'is_closed': False,
                  'v': '5.131'}
        requests_json = requests.get(f'{self.host}/users.search', params=params).json()
        response = requests_json['response']
        infos = response['items']
        candidates_ids = [info['id'] for info in infos if not info['is_closed']]
        return candidates_ids

    def photos_ids(self, candidate_id):
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
        photos_ids = [info['id'] for info in infos[:COUNT_PHOTO]]
        return photos_ids

    def show_candidate(self, candidate_id, photos_ids):
        params = {'user_ids': candidate_id,
                  'fields': 'sex',
                  'access_token': self.token,
                  'v': '5.131'}
        address = {1: 'её', 2: 'его'}
        requests_json = requests.get(f'{self.host}/users.get', params=params).json()
        response = requests_json['response']
        response_open = response[0]
        first_name = response_open['first_name']
        last_name = response_open['last_name']
        sex = response_open['sex']
        user_id = response_open['id']
        name = f'''Имя кандидата: {first_name} {last_name}
                   Ссылка на {address[sex]} профиль: https://vk.com/id{user_id}'''
        attachments = [f'photo{candidate_id}_{photo_id}' for photo_id in photos_ids]
        attachments = ','.join(attachments)
        return name, attachments
