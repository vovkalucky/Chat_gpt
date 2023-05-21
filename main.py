import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers import other_handlers, user_handlers
from bot.keyboards.set_menu import set_main_menu
from bot.models import models
import logging
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
    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    models.sql_start()

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as _ex:
        print(f'There is exception - {_ex}')


# Запускаем поллинг
if __name__ == '__main__':
    asyncio.run(main())
# executor.start_polling(dp, skip_updates=True)


