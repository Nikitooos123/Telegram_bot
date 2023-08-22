import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import game_handler, base_handler


async def main() -> None:

    # Загружаем конфг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tgbot.token)
    dp: Dispatcher = Dispatcher()

    # Иницилизируем роутеры в диспетчере
    dp.include_router(game_handler.router)
    dp.include_router(base_handler.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())