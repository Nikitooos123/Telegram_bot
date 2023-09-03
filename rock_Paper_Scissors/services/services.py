import random

from lexicon.lexicon import LEXICON_RU

# Функция случайного выбора бота в игре
def bot_choise() -> str:
    return random.choice(['rock', 'paper', 'scissors'])

# Возвращает ключ нашего ответа
def get_key(user_choise: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_choise:
            break
    return key

# Определение победителя
def determination_of_the_winner(user_choise: str, bot_choise: str) -> str:
    rules = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    user = get_key(user_choise)
    if rules[user] == bot_choise:
        return 'user_won'
    elif user == bot_choise:
        return 'nobody_won'
    else:
        return 'bot_won'