from Bot import Bot
from API import app
import tokens


if __name__ == '__main__':
    token_for_bot = f'{tokens.BOT_TOKEN}'
    token_for_get = f'{tokens.GET_TOKEN}'
    print('START')
    vk_bot = Bot(token_for_bot, token_for_get)
    # app.run(debug=True)
    vk_bot.bot_start()

