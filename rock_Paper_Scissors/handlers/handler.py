from aiogram import Router
from aiogram.filters import Text, Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup

import random
from keyboards.keyboard import yes_no_kb, game_kb
from lexicon.lexicon import LEXICON_RU
from services.services import bot_choise, determination_of_the_winner
router: Router = Router()

# Хендлер срабатывает на комманду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)

# Хендлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)

# Хендлер срабатывает на согласие играть
@router.message(Text(text=LEXICON_RU['yes_button']))
async def process_game_command(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)

# Хендлер срабатывать на отказ играть
@router.message(Text(text=LEXICON_RU['no_button']))
async def process_game_command(message: Message):
    await message.answer(text=LEXICON_RU['no'], reply_markup=yes_no_kb)

# Хендлер срабатыват на любой выбор игровой кнопки
@router.message(Text(text=[LEXICON_RU['rock'], LEXICON_RU['paper'], LEXICON_RU['scissors']]))
async def game_process(message: Message):
    bot_selection = bot_choise()
    winner = determination_of_the_winner(message.text, bot_selection)
    await message.answer(text=LEXICON_RU['bot_choice'] + ': ' + bot_selection)
    await  message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)


# Хендлер срабатывает на остальные сообщения
@router.message()
async def other_text_process(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])