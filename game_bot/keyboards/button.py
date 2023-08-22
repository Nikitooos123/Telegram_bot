from aiogram.types import KeyboardButton

# Кнопки
play_game = [KeyboardButton(text='Хочу играть!')]
clue = [KeyboardButton(text='/help')]
statistics = [KeyboardButton(text='/stat')]
exit = [KeyboardButton(text='/cancel')]
attemps = [KeyboardButton(text='/attemps')]
rating = [KeyboardButton(text='/rating')]

# Конфигурации меню
key0 = [play_game, clue + statistics]
key1 = [play_game, statistics + attemps]
key2 = [play_game, clue + rating]
key3 = [exit + clue + statistics]
key4 = [play_game, exit + clue + statistics]
key5 = [play_game, clue + statistics]

