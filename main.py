import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers import other_handlers, user_handlers, admin_handlers
from bot.keyboards.set_menu import set_main_menu
import logging
from aiogram.fsm.storage.memory import MemoryStorage


# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main() -> None:
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    load_dotenv('.env')
    bot: Bot = Bot(token=os.getenv("API_TOKEN"), parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_routers(admin_handlers.router, user_handlers.router, other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        # dp.resolve_used_update_types() Прием только зарегистрированных апдейтов
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as _ex:
        print(f'There is exception - {_ex}')


# Запускаем поллинг
if __name__ == '__main__':
    asyncio.run(main())


