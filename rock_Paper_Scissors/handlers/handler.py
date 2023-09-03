from aiogram import Router
from aiogram.filters import Text, Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup

import random
from keyboards.keyboard import yes_no_kb, game_kb
from lexicon.lexicon import LEXICON_RU
router: Router = Router()

kb = {
    'Kaмeнь': 'Бумага',
    'Бумага': 'Ножницы',
    'Ножницы': 'Камень'
}

def random_list() -> str:
    return random.choice(['Kaмeнь', 'Ножницы', 'Бумага'])

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)

@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)

@router.message(Text(text=LEXICON_RU['yes_button']))
async def process_game_command(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)

@router.message(Text(text=LEXICON_RU['no_button']))
async def process_game_command(message: Message):
    await message.answer(text=LEXICON_RU['no'], reply_markup=yes_no_kb)

@router.message(Text(text=[LEXICON_RU['rock'], LEXICON_RU['paper'], LEXICON_RU['scissors']]))
async def game_process(message: Message):
    bot_selection = random_list()
    await message.answer(text=LEXICON_RU['bot_choice'] + ': ' + bot_selection)

    if kb[message.text] == bot_selection:
        await message.answer(text=LEXICON_RU['bot_won'], reply_markup=yes_no_kb)

    elif kb[bot_selection] == message.text:
        await message.answer(text=LEXICON_RU['user_won'], reply_markup=yes_no_kb)

    elif message.text == bot_selection:
        await message.answer(text=LEXICON_RU['nobody_won'], reply_markup=yes_no_kb)



@router.message()
async def other_text_process(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])