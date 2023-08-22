from dataclasses import dataclass
from environs import Env
import pickle

# Загружаем токен
@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tgbot: TgBot

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tgbot=TgBot(token=env('BOT_TOKEN')))

# Загружаем базу данных
try:
    with open('data.pickle', 'rb') as file:
        users: dict = pickle.load(file)
except FileNotFoundError:
    users: dict = {}

def save():
    with open('data.pickle', 'wb') as file:
        pickle.dump(users, file)