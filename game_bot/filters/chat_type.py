from config_data.config import users
from aiogram.filters import BaseFilter
from aiogram.types import Message

# Фильтры для хендлеров
class KnownUsers(BaseFilter):
    def __int__(self, name):
        self.name = name

    async def __call__(self, message: Message) -> bool:
        try:
            return users[message.from_user.id]['in_game']
        except KeyError:
            return False

class Users(BaseFilter):
    def __int__(self, name):
        self.name = name

    async def __call__(self, message: Message) -> bool:
        try:
            return not users[message.from_user.id]['in_game']
        except KeyError:
            return True