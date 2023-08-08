from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import Text, Command
import random
from TOKEN_API import API_TOKEN
import button
from data import users, save

url = 'https://tenor.com/ru/view/bear-clapping-clap-yay-hooray-gif-5605760'
# Создаем объекты бота и деспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

ATTEMPS: int = 0

def random_number() -> int:
    return random.randint(1, 100)

@dp.message(Command(commands=['start']))
async def start_game(message:Message):
    print(message.json(indent=4, exclude_none=True, ensure_ascii=False))
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

@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key1, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать \nУ вас есть {users[message.from_user.id]["attemps"]} '
                         f'попыток\n\nДоступные команды:\n/help - правила\n'
                         f'/stat - посмотреть статитику\n/attempts - Изменить количество попыток\n\n'
                         f'Давай сыграем?', reply_markup=keyboard)

@dp.message(Command(commands=['attemps']))
async def attemps_command(message: Message):
    await message.answer('Укажите желаемое количество попыток от 1 до 10')

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 10 and not users[x.from_user.id]['in_game'])
async def change_attems(message: Message):
    users[message.from_user.id]['attemps'] = int(message.text)
    await message.answer(f'Количество попыток изменено на {users[message.from_user.id]["attemps"]}')

@dp.message(Command(commands=['stat']))
async def start_game(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key2, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["win"]}\n'
                         f'Количество используемых попыток: {users[message.from_user.id]["attemps"]}', reply_markup=keyboard)

@dp.message(Command(commands=['rating']))
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

@dp.message(Command(commands=['cancel']))
async def cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть'
                             'снова - напишите об этом')
    else:
        await message.answer('А мы с вами не играем'
                             'Moжет, сыграем разок?')

@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть!'], ignore_case=True))
async def process_game(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key3, resize_keyboard=True, one_time_keyboard=True)
    if not users[message.from_user.id]['in_game']:
        await message.answer('Ура\n\nЯ загадал число от 1 до 100, '
                             'попробуй угадать!', reply_markup=keyboard)
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = random_number()
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на числа от 1 до 100'
                             'и команды /cancel и /start')

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers(message: Message):
    global ATTEMPS
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

@dp.message()
async def other_text_proess(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=button.key0, resize_keyboard=True, one_time_keyboard=True)
    if users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'Просто сыграем в игру?', reply_markup=keyboard)

if __name__ == '__main__':
    dp.run_polling(bot)