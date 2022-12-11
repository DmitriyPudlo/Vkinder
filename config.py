import Keyboard

FAVOR_COMMANDS_VK = {
    False: (Keyboard.response_favor_without_candidates_key, Keyboard.favor_ending_without_candidates_key),
    True: (Keyboard.response_favor_key, Keyboard.favor_ending_key)}

FAVOR_COMMANDS = {
    False: Keyboard.favor_ending_without_candidates,
    True: Keyboard.favor_ending}

ADDRESS = {1: 'её', 2: 'его'}
