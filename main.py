from Bot import Bot
from VK import VK
from BD import show_favor_bd
import Keyboard


def show_favor(key_begin, key_end):
    favor_ids = show_favor_bd()
    for favor_id in favor_ids:
        favor_photos_ids = get.photos_ids(favor_id)
        favor_to_bot = get.show_candidate(favor_id, favor_photos_ids)
        vk_bot.response_favor(favor_to_bot)
        vk_bot.show_key(key_begin)
        answer = vk_bot.speak()
        if answer == 'Продолжить просмотр кандидатов':
            return
    else:
        vk_bot.favor_ending()
        vk_bot.show_key(key_end)
        return vk_bot.speak()


if __name__ == '__main__':
    token_for_bot = 'vk1.a.JxoJoWFTReNOLAljFNSnro8hPf-id5kL96fZMNav2GpjCkRyq-nCjfzKZ7Qw0JGLaqvaGkCGxaQd9wu5gFbbe-lJ9SI8V1ylZAU8b5UtHKuyE7LYY7leev62QD56yu9fVwsmYRhSyPDevWqdjI3QwJwIEV_bHqEPQ8i_-Fh-W0OVYQBk4xuPHfDUq9CbMSFD'
    token_for_get = 'vk1.a.91ZpDzsxgBpqsfabik3ZtJXTQmHr_NwlABJc3-NJwylWyWrHEF78HHofS5nTyFeKSe0JmmOU9oKjlBp9gceEjNJFSYYs6Qe25z65hTNUVfrvNLBZMgqHCrqz-nvAgMLZ5_4zLjBVgwfhKpEk7aBAh1-s0-Xq6dFygbEnP17tSAFRSDGmN5hJxqMtlLj3xPKR'
    print('START')
    vk_bot = Bot(token_for_bot)
    get = VK(token_for_get)
    while True:
        client_id = vk_bot.greeting()
        vk_bot.start()
        while True:
            criteria_search = get.search_client_info(client_id)
            candidates_ids = get.search_candidate(criteria_search)
            for id_candidate in candidates_ids:
                photos_ids = get.photos_ids(id_candidate)
                to_bot = get.show_candidate(id_candidate, photos_ids)
                vk_bot.response(to_bot)
                vk_bot.show_key(Keyboard.response_key())
                command = vk_bot.speak(id_candidate)
                if command == "Показать избранных":
                    response_favor = Keyboard.response_favor()
                    favor_ending = Keyboard.favor_ending_key()
                    show_favor(response_favor, favor_ending)
                elif command == "Стоп":
                    break
            else:
                vk_bot.ending()
                vk_bot.show_key(Keyboard.ending_key())
                command = vk_bot.speak()
                if command == "Показать избранных":
                    favor_without_candidates = Keyboard.response_favor_without_candidates()
                    favor_ending_without_candidates = Keyboard.favor_ending_without_candidates()
                    show_favor(favor_without_candidates, favor_ending_without_candidates)
            break
