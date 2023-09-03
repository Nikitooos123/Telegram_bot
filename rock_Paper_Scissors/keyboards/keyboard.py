from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
# from aiogram.utils.keyboard import ReplyKeyboardMarkup

from lexicon.lexicon import LEXICON_RU

button_yes = [KeyboardButton(text=LEXICON_RU['yes_button'])]
button_no = [KeyboardButton(text=LEXICON_RU['no_button'])]
help = [KeyboardButton(text='/help')]
button_1 = [KeyboardButton(text=LEXICON_RU['rock'])]
button_2 = [KeyboardButton(text=LEXICON_RU['scissors'])]
button_3 = [KeyboardButton(text=LEXICON_RU['paper'])]

yes_no_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[button_yes, button_no],
                                                     resize_keyboard=True)

game_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[button_1, button_2, button_3],
                                                   resize_keyboard=True)
