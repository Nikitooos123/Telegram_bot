from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

# Клавиатура с билдером
button_yes: KeyboardButton = KeyboardButton(text=LEXICON_RU['yes_button'])
button_no: KeyboardButton = KeyboardButton(text=LEXICON_RU['no_button'])

# Иницилизируем билдер
yes_no_kb_bilder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер
yes_no_kb_bilder.row(button_yes, button_no, width=2)

# Создаем клавиатурус кнопками "Давай" и "Не хочу"
yes_no_kb: ReplyKeyboardMarkup = yes_no_kb_bilder.as_markup(one_time_keyboard=True, resize_keyboard=True)

# Клавиатура без билдера
# Кнопки
button_1: list[KeyboardButton] = [KeyboardButton(text=LEXICON_RU['rock'])]
button_2: list[KeyboardButton] = [KeyboardButton(text=LEXICON_RU['scissors'])]
button_3: list[KeyboardButton] = [KeyboardButton(text=LEXICON_RU['paper'])]

# Создаем клавиатуру с кнопками "Камень", "Ножницы" и "Бумага"
game_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[button_1, button_2, button_3],
                                                   resize_keyboard=True)
