from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.types import Message, ReplyKeyboardMarkup

from config_data.config import users
from keyboards import button
from filters.chat_type import Users
import random

router: Router = Router()
router.message.filter(Users())
# Создание рандомного числа
def random_number() -> int:
    return random.randint(1, 100)

# Стартовый хендлер
@router.message(Command(commands=['start']))
async def start_game(message:Message):
    # print(message.json())
    keyboard = ReplyKeyboardMarkup(keyboard=button.key0, resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Привт!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправь команду /help', reply_markup=keyboard)

    if message.from_user.id not in users:
        users[message.from_user.id] = {
                'name_user': message.from_user.first_name + ' ' + message.from_user.last_name,
                'in_game': False,
                'secret_number': None,
                'attemps': 7,
                'ATTEMPS': 0,
                'total_games': 0,
                'win': 0
        }

# Что умеет бот
@router.message(Command(commands=['help']))
async def help_command(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key1, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать \nУ вас есть {users[message.from_user.id]["attemps"]} '
                         f'попыток\n\nДоступные команды:\n/help - правила\n'
                         f'/stat - посмотреть статитику\n/attempts - Изменить количество попыток\n\n'
                         f'Давай сыграем?', reply_markup=keyboard)

# Изменяем количество попыток
@router.message(Command(commands=['attemps']))
async def attemps_command(message: Message):
    users[message.from_user.id]['ATTEMPS'] = True
    await message.answer('Укажите желаемое количество попыток от 1 до 10')

@router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 10 and users[x.from_user.id]['ATTEMPS'])
async def change_attems(message: Message):
    users[message.from_user.id]['attemps'] = int(message.text)
    users[message.from_user.id]['ATTEMPS'] = 0
    await message.answer(f'Количество попыток изменено на {users[message.from_user.id]["attemps"]}')

# Статистика игрока
@router.message(Command(commands=['stat']))
async def start_game(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key2, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["win"]}\n'
                         f'Количество используемых попыток: {users[message.from_user.id]["attemps"]}', reply_markup=keyboard)

# Рейтинг игроков
@router.message(Command(commands=['rating']))
async def rating_top(message: Message):
    top = 'Рейтинг игроков:\n\n'
    list_id = []
    for item_id in users.keys():
        if len(list_id) == 0:
            list_id.append(item_id)
            continue
        for number in range(len(list_id)):
            if int(users[item_id]['win']) > int(users[list_id[number]]['win']):
                list_id.insert(number, item_id)
            elif number + 1 == len(list_id):
                list_id.append(item_id)

    for item in list_id:
        top += f'{users[item]["name_user"]} - победы {users[item]["win"]}\n'
    await message.answer(top)

# Завершение игры
@router.message(Command(commands=['cancel']))
async def cancel_command(message: Message):
    await message.answer('А мы с вами не играем'
                        'Moжет, сыграем разок?')

# Старт игры
@router.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть!'], ignore_case=True))
async def process_game(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key3, resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Ура\n\nЯ загадал число от 1 до 100, '
                        'попробуй угадать!', reply_markup=keyboard)
    users[message.from_user.id]['in_game'] = True
    users[message.from_user.id]['secret_number'] = random_number()



# Принимает остальные сообщения
@router.message()
async def other_text_proess(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key0, resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Я довольно ограниченный бот, давайте '
                             'Просто сыграем в игру?', reply_markup=keyboard)