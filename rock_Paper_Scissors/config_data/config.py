from dataclasses import dataclass
from environs import Env

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