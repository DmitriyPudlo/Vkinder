from Bot import Bot


if __name__ == '__main__':
    token_for_bot = ''
    token_for_get = ''
    print('START')
    vk_bot = Bot(token_for_bot, token_for_get)
    vk_bot.bot_start()
