from Bot import Bot
from VK import VK

if __name__ == '__main__':
    token_for_bot = ''
    token_for_get = ''
    print('START')
    vk_bot = Bot(token_for_bot)
    get = VK(token_for_get)
    client_id = vk_bot.greeting()
    while True:
        criteria_search = get.search_client_info(client_id)
        candidates_ids = get.search_candidate(criteria_search)
        for id_candidate in candidates_ids:
            photos_ids = get.photos_ids(id_candidate)
            to_bot = get.show_candidate(id_candidate, photos_ids)
            answer = vk_bot.response(to_bot)
            command = vk_bot.speak()
            if command == 'СЛЕДУЮЩИЙ':
                continue
            elif command == 'СТОП':
                break
        else:
            vk_bot.ending()

