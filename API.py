from VK import VK
import tokens
import vk_api

vk = VK(tokens.GET_TOKEN)


def prepare_info(candidate_id, response, photos_ids):
    first_name = response['first_name']
    last_name = response['last_name']
    user_id = response['id']
    photos_url = [f'https://vk.com/photo{candidate_id}_{photo_id}' for photo_id in photos_ids]
    photos_url = ','.join(photos_url)
    info = {'first_name': first_name,
            'last_name': last_name,
            'url': user_id,
            'photos_url': photos_url}
    return info


