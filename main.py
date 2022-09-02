from Bot import Bot


if __name__ == '__main__':
    token_for_bot = 'vk1.a.JxoJoWFTReNOLAljFNSnro8hPf-id5kL96fZMNav2GpjCkRyq-nCjfzKZ7Qw0JGLaqvaGkCGxaQd9wu5gFbbe-lJ9SI8V1ylZAU8b5UtHKuyE7LYY7leev62QD56yu9fVwsmYRhSyPDevWqdjI3QwJwIEV_bHqEPQ8i_-Fh-W0OVYQBk4xuPHfDUq9CbMSFD'
    token_for_get = 'vk1.a.91ZpDzsxgBpqsfabik3ZtJXTQmHr_NwlABJc3-NJwylWyWrHEF78HHofS5nTyFeKSe0JmmOU9oKjlBp9gceEjNJFSYYs6Qe25z65hTNUVfrvNLBZMgqHCrqz-nvAgMLZ5_4zLjBVgwfhKpEk7aBAh1-s0-Xq6dFygbEnP17tSAFRSDGmN5hJxqMtlLj3xPKR'
    print('START')
    vk_bot = Bot(token_for_bot, token_for_get)
    vk_bot.bot_start()
