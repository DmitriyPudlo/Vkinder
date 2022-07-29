from vk_api.keyboard import VkKeyboard


def create_keyboard(button_names):
    keyboard = VkKeyboard(one_time=True)
    for button_name in button_names:
        keyboard.add_button(button_name)
    keyboard = keyboard.get_keyboard()
    return keyboard


greeting = ['Старт']
response = ['Следующий', "Стоп", "Добавить в избранные", "Показать избранных"]
ending = ["Показать избранных", "Стоп"]
favor_ending = ['Продолжить просмотр кандидатов']
add_favor = ['Следующий', "Стоп", "Показать избранных"]
response_favor = ['Следующий из списка избранных', 'Продолжить просмотр кандидатов']
response_favor_without_candidates = ['Следующий из списка избранных']
favor_ending_without_candidates = ['Стоп']

greeting_key = create_keyboard(greeting)
response_key = create_keyboard(response)
ending_key = create_keyboard(ending)
favor_ending_key = create_keyboard(favor_ending)
add_favor_key = create_keyboard(add_favor)
response_favor_key = create_keyboard(response_favor)
response_favor_without_candidates_key = create_keyboard(response_favor_without_candidates)
favor_ending_without_candidates_key = create_keyboard(favor_ending_without_candidates)
