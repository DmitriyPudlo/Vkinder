from vk_api.keyboard import VkKeyboard


def VkKeyboard_get(func):
    def wrapper(*args, **kwargs):
        keyboard = func(*args, **kwargs)
        keyboard = keyboard.get_keyboard()
        return keyboard
    return wrapper


@VkKeyboard_get
def greeting_key():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Старт') #после реализации кнопок ниже - удалить
    # keyboard.add_button('Задать критерии поиска')
    # keyboard.add_button('Поиск по-умолчанию')
    # keyboard.add_button('Показать избранных')
    return keyboard


@VkKeyboard_get
def response_key():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Следующий')
    keyboard.add_button('Стоп')
    keyboard.add_button('Добавить в избранные')
    keyboard.add_button('Показать избранных')
    return keyboard


@VkKeyboard_get
def ending_key():
    keyboard = VkKeyboard(one_time=True)
    # keyboard.add_button('ЗАДАТЬ НОВЫЕ КРИТЕРИИ')
    keyboard.add_button('Показать избранных')
    keyboard.add_button('Стоп')
    return keyboard


@VkKeyboard_get
def favor_ending_key():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Продолжить просмотр кандидатов')
    return keyboard


@VkKeyboard_get
def add_favor_key():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Следующий')
    keyboard.add_button('Стоп')
    keyboard.add_button('Показать избранных')
    return keyboard


@VkKeyboard_get
def response_favor():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Следующий из списка избранных')
    keyboard.add_button('Продолжить просмотр кандидатов')
    return keyboard


@VkKeyboard_get
def response_favor_without_candidates():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Следующий из списка избранных')
    return keyboard


@VkKeyboard_get
def favor_ending_without_candidates():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Стоп')
    return keyboard