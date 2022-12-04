from Bot import Bot
from API import app
from Telegram import Telegram, tele_bot
import tokens


if __name__ == '__main__':
    token_for_bot = f'{tokens.BOT_TOKEN}'
    token_for_get = f'{tokens.GET_TOKEN}'
    print('START')
    vk_bot = Bot(token_for_bot, token_for_get)
    telegram = Telegram(token_for_get)
    vk_bot.bot_start()
    app.run(debug=True)
    tele_bot.polling(none_stop=True)


