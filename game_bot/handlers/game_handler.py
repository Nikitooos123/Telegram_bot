from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.types import Message, ReplyKeyboardMarkup
from config_data.config import save, users
from keyboards import button
from filters.chat_type import KnownUsers

router: Router = Router()
# Ссылка на гифку

url = 'https://tenor.com/ru/view/bear-clapping-clap-yay-hooray-gif-5605760'
router.message.filter(KnownUsers())

# Хендлер принимает числа во время игры
@router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key4, resize_keyboard=True, one_time_keyboard=True)
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer_document(document=url)
            await message.answer('Ура!!! Вы угадали число!\n\n'
                                 'Может сыграем еще?', reply_markup=keyboard)
            users[message.from_user.id]['ATTEMPS'] = 0
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['win'] += 1
            save()
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Мое число меньше')
            users[message.from_user.id]['ATTEMPS'] += 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Мое число больше')
            users[message.from_user.id]['ATTEMPS'] += 1

        if users[message.from_user.id]['attemps'] == users[message.from_user.id]['ATTEMPS']:
            await message.answer('К сожалению у вас больше не осталось'
                                 'попыток. Вы проиграли :(\n\nМое число '
                                 f'было {users[message.from_user.id]["secret_number"]}\n\nДавайте '
                                 'сыграем еще?', reply_markup=keyboard)
            users[message.from_user.id]['ATTEMPS'] = 0
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            save()
    else:
        keyboard = ReplyKeyboardMarkup(keyboard=button.key0, resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Мы еще не играем. Хотите сыграть?', reply_markup=keyboard)

# Завершение игры
@router.message(Command(commands=['cancel']))
async def cancel_command(message: Message):
    users[message.from_user.id]['ATTEMPS'] = 0
    users[message.from_user.id]['in_game'] = False
    await message.answer('Вы вышли из игры. Если захотите сыграть'
                        'снова - напишите об этом')

# Старт игры
@router.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть!'], ignore_case=True))
async def process_game(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key3, resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Пока мы играем в игру я могу '
                         'реагировать только на числа от 1 до 100'
                         'и команду /cancel')

# Принимает остальные сообщения
@router.message()
async def other_text_proess(message: Message):
    await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
