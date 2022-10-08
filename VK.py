import requests
from datetime import date, datetime

COUNT_CANDIDATE = 100
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

    def __search_by_params(self, params):
        requests_json = requests.get(f'{self.host}/users.search', params=params).json()
        response = requests_json['response']
        infos = response['items']
        return infos

    def search_candidate(self, criteria, count=None):
        if not count:
            count = COUNT_CANDIDATE
        print(count)
        params = {'count': count,
                  'city': criteria['city'],
                  'sex': criteria['sex'],
                  'status': IN_SEARCH,
                  'age_from': criteria['age'] - 3,
                  'age_to': criteria['age'] + 3,
                  'has_photo': WITH_PHOTO,
                  'access_token': self.token,
                  'is_closed': False,
                  'v': '5.131'}
        infos = self.__search_by_params(params)
        candidates_ids = [info['id'] for info in infos if not info['is_closed']]
        if len(candidates_ids) != count:
            while True:
                params['offset'] = count
                infos = self.__search_by_params(params)
                for info in infos:
                    if not info['is_closed']:
                        candidates_ids.append(info['id'])
                        if len(candidates_ids) == count:
                            return candidates_ids
                count += count
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

    def show_candidate(self, candidate_id):
        params = {'user_ids': candidate_id,
                  'fields': 'sex',
                  'access_token': self.token,
                  'v': '5.131'}
        requests_json = requests.get(f'{self.host}/users.get', params=params).json()
        response = requests_json['response']
        response_open = response[0]
        result = {'first_name': response_open['first_name'],
                  'last_name': response_open['last_name'],
                  'sex': response_open['sex']}
        return result
