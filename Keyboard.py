from vk_api.keyboard import VkKeyboard


def create_keyboard(button_names):
    keyboard = VkKeyboard(one_time=True)
    for button_name in button_names:
        keyboard.add_button(button_name)
    keyboard = keyboard.get_keyboard()
    return keyboard


class Keyword:
    START = 'Старт'
    NEXT = 'Следующий'
    STOP = "Стоп"
    ADD_FAVOR = "Добавить в избранные"
    SHOW_FAVOR = "Показать избранных"
    CONTINUE = 'Продолжить просмотр кандидатов'
    NEXT_FAVOR = 'Следующий из списка избранных'


greeting = [Keyword.START]
response = [Keyword.NEXT, Keyword.STOP, Keyword.ADD_FAVOR, Keyword.SHOW_FAVOR]
ending = [Keyword.SHOW_FAVOR, Keyword.STOP]
favor_ending = [Keyword.CONTINUE]
add_favor = [Keyword.NEXT, Keyword.STOP, Keyword.SHOW_FAVOR]
response_favor = [Keyword.NEXT_FAVOR, Keyword.CONTINUE]
response_favor_without_candidates = [Keyword.NEXT_FAVOR]
favor_ending_without_candidates = [Keyword.STOP]

greeting_key = create_keyboard(greeting)
response_key = create_keyboard(response)
ending_key = create_keyboard(ending)
favor_ending_key = create_keyboard(favor_ending)
add_favor_key = create_keyboard(add_favor)
response_favor_key = create_keyboard(response_favor)
response_favor_without_candidates_key = create_keyboard(response_favor_without_candidates)
favor_ending_without_candidates_key = create_keyboard(favor_ending_without_candidates)
